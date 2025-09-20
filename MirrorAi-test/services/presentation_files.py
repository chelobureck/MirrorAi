"""
Presentation Files Service - хранение raw.html и final.html
"""
import os
import uuid
from pathlib import Path
from typing import Optional
import aiofiles

class PresentationFilesService:
    """Сервис для работы с файлами презентаций"""
    
    def __init__(self, base_path: str = "presentations"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def _get_presentation_dir(self, user_or_guest_id: str, presentation_id: str) -> Path:
        """Получить директорию для презентации"""
        presentation_dir = self.base_path / user_or_guest_id / presentation_id
        presentation_dir.mkdir(parents=True, exist_ok=True)
        return presentation_dir
    
    async def save_raw_html(self, user_or_guest_id: str, presentation_id: str, html_content: str) -> str:
        """
        Сохранить черновой HTML
        Возвращает путь к файлу
        """
        presentation_dir = self._get_presentation_dir(user_or_guest_id, presentation_id)
        raw_file_path = presentation_dir / "raw.html"
        
        async with aiofiles.open(raw_file_path, 'w', encoding='utf-8') as f:
            await f.write(html_content)
        
        return str(raw_file_path)
    
    async def save_final_html(self, user_or_guest_id: str, presentation_id: str, html_content: str) -> str:
        """
        Сохранить финальный HTML с картинками
        Возвращает путь к файлу
        """
        presentation_dir = self._get_presentation_dir(user_or_guest_id, presentation_id)
        final_file_path = presentation_dir / "final.html"
        
        async with aiofiles.open(final_file_path, 'w', encoding='utf-8') as f:
            await f.write(html_content)
        
        return str(final_file_path)
    
    async def get_raw_html(self, user_or_guest_id: str, presentation_id: str) -> Optional[str]:
        """Получить черновой HTML"""
        presentation_dir = self._get_presentation_dir(user_or_guest_id, presentation_id)
        raw_file_path = presentation_dir / "raw.html"
        
        if not raw_file_path.exists():
            return None
        
        async with aiofiles.open(raw_file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    
    async def get_final_html(self, user_or_guest_id: str, presentation_id: str) -> Optional[str]:
        """Получить финальный HTML"""
        presentation_dir = self._get_presentation_dir(user_or_guest_id, presentation_id)
        final_file_path = presentation_dir / "final.html"
        
        if not final_file_path.exists():
            return None
        
        async with aiofiles.open(final_file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    
    def delete_presentation_files(self, user_or_guest_id: str, presentation_id: str) -> bool:
        """Удалить все файлы презентации"""
        try:
            presentation_dir = self._get_presentation_dir(user_or_guest_id, presentation_id)
            if presentation_dir.exists():
                import shutil
                shutil.rmtree(presentation_dir)
            return True
        except Exception as e:
            print(f"Error deleting presentation files: {e}")
            return False
    
    def get_presentation_info(self, user_or_guest_id: str, presentation_id: str) -> dict:
        """Получить информацию о файлах презентации"""
        presentation_dir = self._get_presentation_dir(user_or_guest_id, presentation_id)
        raw_file = presentation_dir / "raw.html"
        final_file = presentation_dir / "final.html"
        
        return {
            "presentation_dir": str(presentation_dir),
            "raw_exists": raw_file.exists(),
            "final_exists": final_file.exists(),
            "raw_size": raw_file.stat().st_size if raw_file.exists() else 0,
            "final_size": final_file.stat().st_size if final_file.exists() else 0,
        }

# Синглтон сервиса
presentation_files_service = PresentationFilesService()
