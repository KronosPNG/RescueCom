class Emergency:
    id: int
    user_uuid: str
    position: tuple[float, float, float]
    address: str
    city: str
    street_number: int
    place_description: str
    photo_b64: str
    resolved: bool
    # TODO: could be a new table
    details_json: str

    def __init__(
        self,
        id: int,
        user_uuid: str,
        address: str,
        city: str,
        street_number: int,
        resolved: bool,
        position: tuple[float, float, float] = (0.0, 0.0, 0.0),
        place_description: str = "",
        photo_b64: str = "",
        details_json: str = "",
    ) -> None:
        self.id = id
        self.user_uuid = user_uuid
        self.position = position
        self.address = address
        self.city = city
        self.street_number = street_number
        self.place_description = place_description
        self.photo_b64 = photo_b64
        self.resolved = resolved
        self.details_json = details_json

    def to_db_tuple(self) -> tuple:
        return (
            self.id,
            self.user_uuid,
            # NOTE: Saved in the db as: "x,y,z"
            f"{self.position[0]},{self.position[1]},{self.position[2]}",
            self.address,
            self.city,
            self.street_number,
            self.place_description,
            self.photo_b64,
            self.resolved,
            self.details_json,
        )
