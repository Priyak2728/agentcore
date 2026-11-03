
from strands import Agent, tool
from strands.multiagent.a2a import A2AServer


# Tool belonging to Airline B
@tool
def check_flight_availability(
    source: str,
    destination: str,
    date: str,
    passengers: int
) -> str:
    """
    Check available seats on Airline B flights.
    """

    print("\nAirline B: Checking its booking system...")

    # Simulated airline inventory
    available_seats = 25
    fare = 45000

    if passengers > available_seats:
        return (
            f"Only {available_seats} seats available. "
            "Cannot accommodate all passengers."
        )

    return f"""
    Airline B Flight Availability:

    Flight Number: PB-205
    Route: {source} to {destination}
    Date: {date}
    Available Seats: {available_seats}
    Requested Passengers: {passengers}
    Fare per passenger: INR {fare}

    Status: Seats available.
    """


# Create Airline B's AI agent
def create_agent(context_id: str) -> Agent:

    return Agent(
        name="Airline B Availability Agent",

        description=(
            "Checks partner airline flight availability "
            "and returns seat and fare information."
        ),

        system_prompt="""
        You are Airline B's Flight Availability Specialist.

        Your responsibility is to:
        1. Understand flight availability requests.
        2. Use the check_flight_availability tool.
        3. Return flight number, available seats and fare.
        4. Clearly explain whether the requested passengers
           can be accommodated.

        Do not invent flight availability information.
        Always use the tool.
        """,

        tools=[check_flight_availability],

        callback_handler=None
    )


# Expose Airline B through A2A
if __name__ == "__main__":

    print("Starting Airline B A2A Server...")

    server = A2AServer(
        agent_factory=create_agent,
        host="127.0.0.1",
        port=9000
    )

    server.serve()
