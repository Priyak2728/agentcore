
import asyncio
import httpx

from uuid import uuid4

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.types import Message, Part, TextPart, Role


async def main():

    partner_url = "http://127.0.0.1:9000"

    async with httpx.AsyncClient(timeout=120) as http_client:

        # STEP 1: Discover Airline B's Agent Card
        print("\nAirline A: Discovering Airline B...")

        resolver = A2ACardResolver(
            httpx_client=http_client,
            base_url=partner_url
        )

        agent_card = await resolver.get_agent_card()

        print("Discovered Agent:", agent_card.name)
        print("Description:", agent_card.description)

        # STEP 2: Create A2A client
        factory = ClientFactory(
            ClientConfig(
                httpx_client=http_client,
                streaming=False
            )
        )

        client = factory.create(agent_card)

        # STEP 3: Prepare request
        message = Message(
            kind="message",
            role=Role.user,
            message_id=uuid4().hex,
            parts=[
                Part(
                    root=TextPart(
                        kind="text",
                        text="""
                        We are Airline A.

                        We need 20 seats on a flight
                        from Mumbai to London on 2026-12-15.

                        Please check your flight availability,
                        flight number and fare.
                        """
                    )
                )
            ]
        )

        # STEP 4: Send request to Airline B
        print("\nAirline A: Sending request to Airline B...")

        async for event in client.send_message(message):

            print("\nAirline A: Response received!")

            print(event)


if __name__ == "__main__":
    asyncio.run(main())
