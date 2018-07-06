import re
from .constants import (SCHEDULE_SCHEME,
                        SCHEDULE_URL)
from datetime import datetime
from pyquery import PyQuery as pq
from sportsreference import utils
from sportsreference.constants import (WIN,
                                       LOSS,
                                       HOME,
                                       AWAY,
                                       NEUTRAL,
                                       REGULAR_SEASON,
                                       CONFERENCE_TOURNAMENT)
from sportsreference.nhl.boxscore import Boxscore
from sportsreference.nhl.constants import OVERTIME_LOSS, SHOOTOUT


class Game(object):
    """
    A representation of a matchup between two teams.

    Stores all relevant high-level match information for a game in a team's
    schedule including date, time, opponent, and result.
    """
    def __init__(self, game_data, year):
        """
        Parse all of the attributes located in the HTML data.

        Parameters
        ----------
        game_data : string
            The row containing the specified game information.
        year : string
            The year of the current season.
        """
        self._game = None
        self._date = None
        self._time = None
        self._boxscore = None
        self._location = None
        self._opponent_abbr = None
        self._opponent_name = None
        self._goals_scored = None
        self._goals_allowed = None
        self._result = None
        self._overtime = None
        self._wins = None
        self._losses = None
        self._overtime_losses = None
        self._streak = None
        self._shots_on_goal = None
        self._penalties_in_minutes = None
        self._power_play_goals = None
        self._power_play_opportunities = None
        self._short_handed_goals = None
        self._attendance = None
        self._length_of_game = None

        self._parse_game_data(game_data)

    def _parse_abbreviation(self, game_data):
        """
        Parses the opponent's abbreviation from their name.

        The opponent's abbreviation is embedded within the HTML tag and needs
        a special parsing scheme in order to be extracted.
        """
        name = game_data('td[data-stat="opp_name"]:first')
        name = re.sub(r'.*/teams/', '', str(name))
        name = re.sub('/.*', '', name)
        setattr(self, '_opponent_abbr', name)

    def _parse_boxscore(self, game_data):
        """
        Parses the boxscore URI for the game.

        The boxscore is embedded within the HTML tag and needs a special
        parsing scheme in order to be extracted.
        """
        boxscore = game_data('td[data-stat="box_score_text"]:first')
        boxscore = re.sub(r'.*/boxscores/', '', str(boxscore))
        setattr(self, '_boxscore', boxscore)

    def _parse_game_data(self, game_data):
        """
        Parses a value for every attribute.

        The function looks through every attribute with the exception of those
        listed below and retrieves the value according to the parsing scheme
        and index of the attribute from the passed HTML data. Once the value
        is retrieved, the attribute's value is updated with the returned
        result.

        Note that this method is called directory once Game is invoked and does
        not need to be called manually.

        Parameters
        ----------
        game_data : string
            A string containing all of the rows of stats for a given game.
        """
        for field in self.__dict__:
            # Remove the leading '_' from the name
            short_name = str(field)[1:]
            if short_name == 'opponent_abbr':
                self._parse_abbreviation(game_data)
                continue
            elif short_name == 'boxscore':
                self._parse_boxscore(game_data)
                continue
            value = utils.parse_field(SCHEDULE_SCHEME, game_data, short_name)
            setattr(self, field, value)

    @property
    def game(self):
        """
        Returns an int to indicate which game in the season was requested. The
        first game of the season returns 1.
        """
        return int(self._game)

    @property
    def date(self):
        """
        Returns a string of the date the game was played, such as '2017-10-05'.
        """
        return self._date

    @property
    def time(self):
        """
        Returns a string of the time the game started, such as '7:00 PM'.
        """
        return self._time

    @property
    def datetime(self):
        """
        Returns a datetime object to indicate the month, day, year, and time
        the game was played at.
        """
        date_string = '%s %s' % (self._date, self._time)
        return datetime.strptime(date_string, '%Y-%m-%d %I:%M %p')

    @property
    def boxscore(self):
        """
        Returns an instance of the Boxscore class containing more detailed
        stats on the game.
        """
        return Boxscore(self._boxscore)

    @property
    def location(self):
        """
        Returns a string constant to indicate whether the game was played at
        home or away.
        """
        if self._location == '@':
            return AWAY
        return HOME

    @property
    def opponent_abbr(self):
        """
        Returns a string of the opponent's 3-letter abbreviation, such as 'NYR'
        for the New York Rangers.
        """
        return self._opponent_abbr

    @property
    def opponent_name(self):
        """
        Returns a string of the opponent's name, such as 'New York Rangers'.
        """
        return self._opponent_name

    @property
    def goals_scored(self):
        """
        Returns an int of the number of goals the team scored during the game.
        """
        return int(self._goals_scored)

    @property
    def goals_allowed(self):
        """
        Returns an int of the number of goals the team allowed during the game.
        """
        return int(self._goals_allowed)

    @property
    def result(self):
        """
        Returns a string constant to indicate whether the team lost in
        regulation, lost in overtime, or won.
        """
        if self._result.lower() == 'w':
            return WIN
        if self._result.lower() == 'l' and \
           self.overtime != 0:
            return OVERTIME_LOSS
        return LOSS

    @property
    def overtime(self):
        """
        Returns an int of the number of overtimes that were played during the
        game, or an int constant if the game went to a shootout.
        """
        if self._overtime.lower() == 'ot':
            return 1
        if self._overtime.lower() == 'so':
            return SHOOTOUT
        if self._overtime == '':
            return 0
        num = re.findall('\d+', self._overtime)
        if len(num) > 0:
            return int(num[0])
        return 0

    @property
    def wins(self):
        """
        Returns an int of the number of games the team has won during the
        season after the conclusion of the requested game.
        """
        return int(self._wins)

    @property
    def losses(self):
        """
        Returns an int of the number of games the team has lost in regulation
        during the season after the conclusion of the requested game.
        """
        return int(self._losses)

    @property
    def overtime_losses(self):
        """
        Returns an int of the number of games the team has lost in overtime
        during the season after the conclusion of the requested game.
        """
        return int(self._overtime_losses)

    @property
    def streak(self):
        """
        Returns a string of the team's winning streak at the conclusion of the
        requested game. Streaks are listed in the format '[W|L] #' (ie. 'W 3'
        for a 3-game winning streak and 'L 2' for a 2-game losing streak).
        """
        return self._streak

    @property
    def shots_on_goal(self):
        """
        Returns an int of the total number of shots on goal the team
        registered.
        """
        return int(self._shots_on_goal)

    @property
    def penalties_in_minutes(self):
        """
        Returns an int of the total number of minutes the team served for
        penalties.
        """
        return int(self._penalties_in_minutes)

    @property
    def power_play_goals(self):
        """
        Returns an int of the number of power play goals the team scored.
        """
        return int(self._power_play_goals)

    @property
    def power_play_opportunities(self):
        """
        Returns an int of the number of power play opportunities the team had.
        """
        return int(self._power_play_opportunities)

    @property
    def short_handed_goals(self):
        """
        Returns an int of the number of shorthanded goals the team scored.
        """
        return int(self._short_handed_goals)

    @property
    def attendance(self):
        """
        Returns an int of the listed attendance for the game.
        """
        attendance = self._attendance.replace(',', '')
        return int(attendance)

    @property
    def length_of_game(self):
        """
        Returns a string of the duration of the game in the format 'H:MM'.
        """
        return self._length_of_game


class Schedule:
    """
    An object of the given team's schedule.

    Generates a team's schedule for the season including wins, losses, and
    scores if applicable.
    """
    def __init__(self, abbreviation, year=None):
        """
        Parameters
        ----------
        abbreviation : string
            A team's short name, such as 'NYR' for the New York Rangers.
        year : string (optional)
            The requested year to pull stats from.
        """
        self._games = []
        self._pull_schedule(abbreviation, year)

    def __getitem__(self, index):
        """
        Return a specified game.

        Returns a specified game as requested by the index number in the array.
        The input index is 0-based and must be within the range of the schedule
        array.

        Parameters
        ----------
        index : int
            The 0-based index of the game to return.

        Returns
        -------
        Game instance
            If the requested game can be found, its Game instance is returned.
        """
        return self._games[index]

    def __call__(self, date):
        """
        Return a specified game.

        Returns a specific game as requested by the passed datetime. The input
        datetime must have the same year, month, and day, but can have any time
        be used to match the game.

        Parameters
        ----------
        date : datetime
            A datetime object of the month, day, and year to identify a
            particular game that was played.

        Returns
        -------
        Game instance
            If the requested game can be found, its Game instance is returned.

        Raises
        ------
        ValueError
            If the requested date cannot be matched with a game in the
            schedule.
        """
        for game in self._games:
            if game.datetime.year == date.year and \
               game.datetime.month == date.month and \
               game.datetime.day == date.day:
                return game
        raise ValueError('No games found for requested date')

    def __repr__(self):
        """Returns a list of all games scheduled for the given team."""
        return self._games

    def __iter__(self):
        """
        Returns an iterator of all of the games scheduled for the given team.
        """
        return iter(self.__repr__())

    def __len__(self):
        """Returns the number of scheduled games for the given team."""
        return len(self.__repr__())

    def _pull_schedule(self, abbreviation, year):
        """
        Parameters
        ----------
        abbreviation : string
            A team's short name, such as 'NYR' for the New York Rangers.
        year : string
            The requested year to pull stats from.
        """
        if not year:
            year = utils.find_year_for_season('nhl')
        doc = pq(SCHEDULE_URL % (year, abbreviation))
        schedule = utils.get_stats_table(doc, 'table#games')

        for item in schedule:
            if 'class="thead"' in str(item):
                continue
            game = Game(item, year)
            self._games.append(game)
