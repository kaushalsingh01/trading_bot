import os
from dotenv import load_dotenv
from binance import AsyncClient
from bot.logging_config import LogManager

class ClientManager:
    def __init__(self, client: AsyncClient, logger):
        self.client = client
        self.logger = logger

    @classmethod
    async def create(cls):
        log_manager = LogManager()
        logger = log_manager.get_logger("ClientManager")

        load_dotenv()
        api_key = os.getenv("API_KEY")
        secret_key = os.getenv("API_SECRET")

        if not api_key or not secret_key:
            logger.error("API_KEY or API_SECRET not set in environment variables")
            raise ValueError("Missing API credentials")

        try:
            client = await AsyncClient.create(api_key, secret_key, testnet=True)
            logger.info("Binance Futures Testnet AsyncClient initialized successfully")
            return cls(client, logger)
        except Exception as e:
            logger.exception("Error initializing Binance AsyncClient")
            raise

    async def close(self):
        await self.client.close_connection()
        self.logger.info("Binance client connection closed")                        