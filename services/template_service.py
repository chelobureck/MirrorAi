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


# Глобальный экземпляр сервиса
template_service = TemplateService()
