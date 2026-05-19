from dataclasses import dataclass

@dataclass
class Artist:
    ArtistId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"
