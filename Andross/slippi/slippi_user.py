from dataclasses import dataclass, field

from Andross.slippi.slippi_ranks import get_rank
from Andross.slippi.slippi_characters import get_character_id, get_character_url


@dataclass
class Characters:
    id: int = 0
    character: str = ''
    game_count: int = 0

    def get_character_icon_url(self):
        return get_character_url(self.character)

    def get_true_character_id(self):
        return get_character_id(self.character)

    def __eq__(self, other):
        return self.character == other.character and self.game_count == other.game_count


@dataclass
class RankedNetplayProfile:
    id: int = None
    rating_ordinal: float = 1100
    rating_update_count: int = None
    wins: int = 0
    losses: int = 0
    daily_global_placement = None
    daily_regional_placement = None
    continent: str = None
    characters: list[Characters] = field(default_factory=list)


@dataclass
class SlippiUser:
    display_name: str = ''
    connect_code: str = ''
    ranked_profile: RankedNetplayProfile = RankedNetplayProfile()

    def __init__(self, slippi_data: dict):

        # Check if dict exists correctly
        if not slippi_data['data']['getConnectCode']:
            return

        # Create local variables to use later
        user_data = slippi_data['data']['getConnectCode']['user']
        ranked_data = user_data['rankedNetplayProfile']

        # Assign nothing if user_data not present
        if not user_data:
            return

        # Assign values from user
        self.display_name = user_data['displayName']
        self.connect_code = user_data['connectCode']['code']

        # Loop through characters in rankedNetplayProfile to generate Characters list
        characters_list = []
        for character in ranked_data['characters']:
            if character:
                characters_list.append(
                    Characters(
                        id=character['id'],
                        character=character['character'],
                        game_count=character['gameCount'])
                )

        self.ranked_profile = RankedNetplayProfile(
            id=int(ranked_data['id'], 16),
            rating_ordinal=ranked_data['ratingOrdinal'],
            rating_update_count=ranked_data['ratingUpdateCount'],
            wins=ranked_data['wins'] or 0,
            losses=ranked_data['losses'] or 0,
            continent=ranked_data['continent'] or 'NONE',
            characters=characters_list
        )
        self.ranked_profile.daily_global_placement = ranked_data['dailyGlobalPlacement'] or 0
        self.ranked_profile.daily_regional_placement = ranked_data['dailyRegionalPlacement'] or 0

    def get_rank(self) -> str:
        # Check if they've played their placement games, or else return 'None'
        if (self.ranked_profile.wins + self.ranked_profile.losses) < 5:
            return 'None'
        return get_rank(self.ranked_profile.rating_ordinal, self.ranked_profile.daily_regional_placement)

    def get_user_profile_page(self) -> str:
        return f'https://slippi.gg/user/{self.connect_code.replace("#", "-")}'

    def get_main_character(self) -> Characters:
        character_to_return = None
        highest_game_count = 0
        for guy in self.ranked_profile.characters:
            if guy.game_count > highest_game_count:
                highest_game_count = guy.game_count
                character_to_return = guy

        return character_to_return
