"""
Image Microservice Integration - интеграция с микросервисом картинок
"""
import httpx
from typing import Optional
from config.settings import get_settings

settings = get_settings()

class ImageMicroserviceClient:
    """Клиент для работы с микросервисом картинок"""
    
    def __init__(self, microservice_url: str = None):
        self.microservice_url = microservice_url or settings.IMAGE_MICROSERVICE_URL
        self.timeout = settings.IMAGE_MICROSERVICE_TIMEOUT
    
    async def process_html_with_images(self, html_content: str, topic: str = "") -> str:
        """
        Отправить HTML в микросервис и получить HTML с валидными URL картинок
        
        Args:
            html_content: Исходный HTML без картинок
            topic: Тема презентации для контекста
            
        Returns:
            HTML с валидными URL изображений
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "html": html_content,
                    "topic": topic,
                    "language": "ru"
                }
                
                response = await client.post(
                    f"{self.microservice_url}/process-html",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("html", html_content)
                else:
                    print(f"Image microservice error: {response.status_code} - {response.text}")
                    return html_content
                    
        except Exception as e:
            print(f"Error calling image microservice: {e}")
            # Fallback: возвращаем исходный HTML если микросервис недоступен
            return html_content
    
    async def health_check(self) -> bool:
        """Проверка доступности микросервиса"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.microservice_url}/health")
                return response.status_code == 200
        except Exception:
            return False

# Синглтон клиента
image_microservice_client = ImageMicroserviceClient()
