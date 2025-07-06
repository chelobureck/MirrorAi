"""
Template Service - сервис для работы с шаблонами презентаций
"""
import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.template import Template
from models.presentation import Presentation
from models.user import User
from schemas.template import TemplateResponse, TemplateDetail, TemplateCreateResponse, TemplateDeleteResponse


# --- Встроенные шаблоны ---
BUILTIN_TEMPLATES = {
    "minimalism": {
        "id": "minimalism",
        "title": "Минимализм",
        "html_content": """
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"UTF-8\">
            <title>{{title}}</title>
            <style>
                body { background: #fff; color: #222; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; }
                .slide { margin: 40px auto; max-width: 700px; background: #f9f9f9; border-radius: 12px; box-shadow: 0 2px 8px #eee; padding: 40px; }
                h2 { border-bottom: 1px solid #eee; margin-bottom: 20px; }
                .content { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <h1 style=\"text-align:center;\">{{title}}</h1>
            {{slides}}
        </body>
        </html>
        """
    },
    "nature": {
        "id": "nature",
        "title": "Природа",
        "html_content": """
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"UTF-8\">
            <title>{{title}}</title>
            <style>
                body { background: linear-gradient(120deg, #a8e063 0%, #56ab2f 100%); color: #234; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; }
                .slide { margin: 40px auto; max-width: 700px; background: rgba(255,255,255,0.85); border-radius: 16px; box-shadow: 0 4px 16px #b2f7ef; padding: 40px; }
                h2 { color: #388e3c; border-bottom: 1px solid #b2f7ef; margin-bottom: 20px; }
                .content { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <h1 style=\"text-align:center; color:#388e3c;\">{{title}}</h1>
            {{slides}}
        </body>
        </html>
        """
    },
    "transport": {
        "id": "transport",
        "title": "Транспорт",
        "html_content": """
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"UTF-8\">
            <title>{{title}}</title>
            <style>
                body { background: #e0eafc; background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%); color: #222; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; }
                .slide { margin: 40px auto; max-width: 700px; background: #fff; border-radius: 16px; box-shadow: 0 4px 16px #b2b2b2; padding: 40px; border-left: 8px solid #1976d2; }
                h2 { color: #1976d2; border-bottom: 1px solid #b2b2b2; margin-bottom: 20px; }
                .content { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <h1 style=\"text-align:center; color:#1976d2;\">{{title}}</h1>
            {{slides}}
        </body>
        </html>
        """
    },
    "it": {
        "id": "it",
        "title": "IT Технологии",
        "html_content": """
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"UTF-8\">
            <title>{{title}}</title>
            <style>
                body { background: #232526; background: linear-gradient(120deg, #232526 0%, #414345 100%); color: #fff; font-family: 'Fira Mono', 'Consolas', monospace; margin: 0; padding: 40px; }
                .slide { margin: 40px auto; max-width: 700px; background: #2c3e50; border-radius: 16px; box-shadow: 0 4px 16px #111; padding: 40px; border-left: 8px solid #00c3ff; }
                h2 { color: #00c3ff; border-bottom: 1px solid #00c3ff; margin-bottom: 20px; }
                .content { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <h1 style=\"text-align:center; color:#00c3ff;\">{{title}}</h1>
            {{slides}}
        </body>
        </html>
        """
    },
    "abstract": {
        "id": "abstract",
        "title": "Абстракция",
        "html_content": """
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"UTF-8\">
            <title>{{title}}</title>
            <style>
                body { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #333; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; }
                .slide { margin: 40px auto; max-width: 700px; background: rgba(255,255,255,0.95); border-radius: 20px; box-shadow: 0 4px 24px #f7971e44; padding: 40px; border-left: 8px solid #ffd200; }
                h2 { color: #f7971e; border-bottom: 1px solid #ffd200; margin-bottom: 20px; }
                .content { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <h1 style=\"text-align:center; color:#f7971e;\">{{title}}</h1>
            {{slides}}
        </body>
        </html>
        """
    },
}

class TemplateService:
    """Сервис для управления шаблонами презентаций"""
    
    @staticmethod
    async def create_template_from_presentation(
        presentation_id: int,
        user_id: int,
        session: AsyncSession
    ) -> TemplateCreateResponse:
        """Создает шаблон из существующей презентации"""
        
        # Получаем оригинальную презентацию
        result = await session.execute(
            select(Presentation).where(
                Presentation.id == presentation_id,
                Presentation.user_id == user_id  # Только владелец может создавать шаблоны
            )
        )
        presentation = result.scalar_one_or_none()
        
        if not presentation:
            raise ValueError("Presentation not found or access denied")
        
        # Генерируем HTML из контента (импортируем функцию из html_generator)
        from routers.html_generator import create_modern_html_presentation
        html_content = create_modern_html_presentation(presentation.content)
        
        # Создаем шаблон
        template = Template(
            public_id=str(uuid.uuid4()),
            title=presentation.content.get("title", "Unnamed Template"),
            name=presentation.content.get("title", "Unnamed Template"),
            content=presentation.content,  # Копируем весь контент
            html_content=html_content,
            original_presentation_id=presentation.id,
            user_id=user_id,
            is_public=True
        )
        
        session.add(template)
        await session.commit()
        await session.refresh(template)
        
        return TemplateCreateResponse(templateId=template.public_id)
    
    @staticmethod
    async def get_template_by_public_id(
        public_id: str,
        session: AsyncSession
    ) -> Optional[TemplateDetail]:
        """Получает шаблон по публичному ID"""
        
        result = await session.execute(
            select(Template).where(
                Template.public_id == public_id,
                Template.is_public == True
            )
        )
        template = result.scalar_one_or_none()
        
        if not template:
            return None
            
        return TemplateDetail(
            templateId=template.public_id,
            html=template.html_content,
            title=template.title
        )
    
    @staticmethod
    async def get_template_html(
        public_id: str,
        session: AsyncSession
    ) -> Optional[str]:
        """Получает HTML шаблона для просмотра"""
        
        result = await session.execute(
            select(Template).where(
                Template.public_id == public_id,
                Template.is_public == True
            )
        )
        template = result.scalar_one_or_none()
        
        return template.html_content if template else None
    
    @staticmethod
    async def delete_template(
        public_id: str,
        user_id: int,
        session: AsyncSession
    ) -> TemplateDeleteResponse:
        """Удаляет шаблон по публичному ID (только владелец)"""
        
        result = await session.execute(
            select(Template).where(
                Template.public_id == public_id,
                Template.user_id == user_id  # Только владелец может удалять
            )
        )
        template = result.scalar_one_or_none()
        
        if not template:
            raise ValueError("Template not found or access denied")
        
        await session.execute(
            delete(Template).where(Template.id == template.id)
        )
        await session.commit()
        
        return TemplateDeleteResponse()
    
    @staticmethod
    async def list_all_templates(
        session: AsyncSession,
        limit: int = 50
    ) -> List[TemplateResponse]:
        """Получает список всех публичных шаблонов"""
        
        result = await session.execute(
            select(Template)
            .where(Template.is_public == True)
            .order_by(Template.created_at.desc())
            .limit(limit)
        )
        templates = result.scalars().all()
        
        return [
            TemplateResponse(
                templateId=template.public_id,
                title=template.title,
                createdAt=template.created_at
            )
            for template in templates
        ]

    @staticmethod
    def get_builtin_template(template_id: str) -> Optional[dict]:
        """Получить встроенный шаблон по ID"""
        return BUILTIN_TEMPLATES.get(template_id)

    @staticmethod
    def list_builtin_templates() -> List[dict]:
        """Список всех встроенных шаблонов"""
        return list(BUILTIN_TEMPLATES.values())

    @staticmethod
    async def create_builtin_templates_in_db(session: AsyncSession, user_id: int = 1):
        """Загрузить все встроенные шаблоны в БД, если их там нет"""
        from models.template import Template
        for tpl in BUILTIN_TEMPLATES.values():
            # Проверяем, есть ли уже такой шаблон
            result = await session.execute(
                select(Template).where(Template.public_id == tpl["id"])
            )
            exists = result.scalar_one_or_none()
            if not exists:
                template = Template(
                    public_id=tpl["id"],
                    title=tpl["title"],
                    name=tpl["title"],
                    content={},
                    html_content=tpl["html_content"],
                    original_presentation_id=0,
                    user_id=user_id,
                    is_public=True
                )
                session.add(template)
        await session.commit()


# Глобальный экземпляр сервиса
template_service = TemplateService()
