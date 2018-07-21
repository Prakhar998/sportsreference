import re
from .constants import PARSING_SCHEME, SEASON_PAGE_URL
from pyquery import PyQuery as pq
from .. import utils
from .schedule import Schedule


class Team:
    """
    An object containing all of a team's season information.

    Finds and parses all team stat information and identifiers, such as rank,
    name, and abbreviation, and sets them as properties which can be directly
    read from for easy reference.
    """
    def __init__(self, team_data, rank, year=None):
        """
        Parse all of the attributes located in the HTML data.

        Once Team is invoked, it parses all of the listed attributes for the
        team which can be found in the passed HTML data. All attributes below
        are properties which can be directly read for easy reference.

        Parameters
        ----------
        team_data : string
            A string containing all of the rows of stats for a given team. If
            multiple tables are being referenced, this will be comprised of
            multiple rows in a single string.
        rank : int
            A team's position in the league based on the number of points they
            obtained during the season.
        year : string (optional)
            The requested year to pull stats from.
        """
        self._year = year
        self._rank = rank
        self._abbreviation = None
        self._name = None
        self._games_played = None
        self._minutes_played = None
        self._field_goals = None
        self._field_goal_attempts = None
        self._field_goal_percentage = None
        self._three_point_field_goals = None
        self._three_point_field_goal_attempts = None
        self._three_point_field_goal_percentage = None
        self._two_point_field_goals = None
        self._two_point_field_goal_attempts = None
        self._two_point_field_goal_percentage = None
        self._free_throws = None
        self._free_throw_attempts = None
        self._free_throw_percentage = None
        self._offensive_rebounds = None
        self._defensive_rebounds = None
        self._total_rebounds = None
        self._assists = None
        self._steals = None
        self._blocks = None
        self._turnovers = None
        self._personal_fouls = None
        self._points = None
        self._opp_field_goals = None
        self._opp_field_goal_attempts = None
        self._opp_field_goal_percentage = None
        self._opp_three_point_field_goals = None
        self._opp_three_point_field_goal_attempts = None
        self._opp_three_point_field_goal_percentage = None
        self._opp_two_point_field_goals = None
        self._opp_two_point_field_goal_attempts = None
        self._opp_two_point_field_goal_percentage = None
        self._opp_free_throws = None
        self._opp_free_throw_attempts = None
        self._opp_free_throw_percentage = None
        self._opp_offensive_rebounds = None
        self._opp_defensive_rebounds = None
        self._opp_total_rebounds = None
        self._opp_assists = None
        self._opp_steals = None
        self._opp_blocks = None
        self._opp_turnovers = None
        self._opp_personal_fouls = None
        self._opp_points = None

        self._parse_team_data(team_data)

    def _parse_team_data(self, team_data):
        """
        Parses a value for every attribute.

        This function looks through every attribute with the exception of
        '_rank' and retrieves the value according to the parsing scheme and
        index of the attribute from the passed HTML data. Once the value is
        retrieved, the attribute's value is updated with the returned result.

        Note that this method is called directly once Team is invoked and does
        not need to be called manually.

        Parameters
        ----------
        team_data : string
            A string containing all of the rows of stats for a given team. If
            multiple tables are being referenced, this will be comprised of
            multiple rows in a single string.
        """
        for field in self.__dict__:
            # The rank attribute is passed directly to the class during
            # instantiation.
            if field == '_rank' or \
               field == '_year':
                continue
            value = utils._parse_field(PARSING_SCHEME,
                                       team_data,
                                       str(field)[1:])
            setattr(self, field, value)

    @property
    def rank(self):
        """
        Returns an int of the team's rank based on the number of points they
        score per game.
        """
        return int(self._rank)

    @property
    def abbreviation(self):
        """
        Returns a string of the team's abbreviation, such as 'DET' for the
        Detroit Pistons.
        """
        return self._abbreviation

    @property
    def schedule(self):
        """
        Returns an instance of the Schedule class containing the team's
        complete schedule for the season.
        """
        return Schedule(self._abbreviation, self._year)

    @property
    def name(self):
        """
        Returns a string of the team's full name, such as 'Detroit Pistons'.
        """
        return self._name

    @property
    def games_played(self):
        """
        Returns an int of the total number of games the team has played during
        the season.
        """
        return int(self._games_played)

    @property
    def minutes_played(self):
        """
        Returns an int of the total number of minutes played by all players on
        the team during the season.
        """
        return int(self._minutes_played)

    @property
    def field_goals(self):
        """
        Returns an int of the total number of field goals the team has made
        during the season.
        """
        return int(self._field_goals)

    @property
    def field_goal_attempts(self):
        """
        Returns an int of the total number of field goals the team has
        attempted during the season.
        """
        return int(self._field_goal_attempts)

    @property
    def field_goal_percentage(self):
        """
        Returns a float of the percentage of field goals made divided by the
        number of attempts. Percentage ranges from 0-1.
        """
        return float(self._field_goal_percentage)

    @property
    def three_point_field_goals(self):
        """
        Returns an int of the total number of three point field goals the team
        has made during the season.
        """
        return int(self._three_point_field_goals)

    @property
    def three_point_field_goal_attempts(self):
        """
        Returns an int of the total number of three point field goals the team
        has attempted during the season.
        """
        return int(self._three_point_field_goal_attempts)

    @property
    def three_point_field_goal_percentage(self):
        """
        Returns a float of the percentage of three point field goals made
        divided by the number of attempts. Percentage ranges from 0-1.
        """
        return float(self._three_point_field_goal_percentage)

    @property
    def two_point_field_goals(self):
        """
        Returns an int of the total number of two point field goals the team
        has made during the season.
        """
        return int(self._two_point_field_goals)

    @property
    def two_point_field_goal_attempts(self):
        """
        Returns an int of the total number of two point field goals the team
        has attempted during the season.
        """
        return int(self._two_point_field_goal_attempts)

    @property
    def two_point_field_goal_percentage(self):
        """
        Returns a float of the percentage of two point field goals made divided
        by the number of attempts. Percentage ranges from 0-1.
        """
        return float(self._two_point_field_goal_percentage)

    @property
    def free_throws(self):
        """
        Returns an int of the total number of free throws made during the
        season.
        """
        return int(self._free_throws)

    @property
    def free_throw_attempts(self):
        """
        Returns an int of the total number of free throw attempts during the
        season.
        """
        return int(self._free_throw_attempts)

    @property
    def free_throw_percentage(self):
        """
        Returns a float of the percentage of free throws made divided by the
        attempts. Percentage ranges from 0-1.
        """
        return float(self._free_throw_percentage)

    @property
    def offensive_rebounds(self):
        """
        Returns an int of the total number of offensive rebounds the team has
        grabbed.
        """
        return int(self._offensive_rebounds)

    @property
    def defensive_rebounds(self):
        """
        Returns an int of the total number of defensive rebounds the team has
        grabbed.
        """
        return int(self._defensive_rebounds)

    @property
    def total_rebounds(self):
        """
        Returns an int of the total number of rebounds the team has grabbed.
        """
        return int(self._total_rebounds)

    @property
    def assists(self):
        """
        Returns an int of the total number of field goals that were assisted.
        """
        return int(self._assists)

    @property
    def steals(self):
        """
        Returns an int of the total number of times the team stole the ball
        from the opponent.
        """
        return int(self._steals)

    @property
    def blocks(self):
        """
        Returns an int of the total number of times the team blocked an
        opponent's shot.
        """
        return int(self._blocks)

    @property
    def turnovers(self):
        """
        Returns an int of the total number of times the team has turned the
        ball over.
        """
        return int(self._turnovers)

    @property
    def personal_fouls(self):
        """
        Returns an int of the total number of times the team has fouled an
        opponent.
        """
        return int(self._personal_fouls)

    @property
    def points(self):
        """
        Returns an int of the total number of points the team has scored during
        the season.
        """
        return int(self._points)

    @property
    def opp_field_goals(self):
        """
        Returns an int of the total number of field goals the opponents made
        during the season.
        """
        return int(self._opp_field_goals)

    @property
    def opp_field_goal_attempts(self):
        """
        Returns an int of the total number of field goals the opponents
        attempted during the season.
        """
        return int(self._opp_field_goal_attempts)

    @property
    def opp_field_goal_percentage(self):
        """
        Returns a float of the percentage of field goals made divided by the
        number of attempts by the opponent. Percentage ranges from 0-1.
        """
        return float(self._opp_field_goal_percentage)

    @property
    def opp_three_point_field_goals(self):
        """
        Returns an int of the total number of three point field goals the
        opponent made during the season.
        """
        return int(self._opp_three_point_field_goals)

    @property
    def opp_three_point_field_goal_attempts(self):
        """
        Returns an int of the total number of three point field goals the
        opponent attempted during the season.
        """
        return int(self._opp_three_point_field_goal_attempts)

    @property
    def opp_three_point_field_goal_percentage(self):
        """
        Returns a float of the percentage of three point field goals made
        divided by the number of attempts by the opponent. Percentage ranges
        from 0-1.
        """
        return float(self._opp_three_point_field_goal_percentage)

    @property
    def opp_two_point_field_goals(self):
        """
        Returns an int of the total number of two point field goals the
        opponent made during the season.
        """
        return int(self._opp_two_point_field_goals)

    @property
    def opp_two_point_field_goal_attempts(self):
        """
        Returns an int of the total number of two point field goals the
        opponent attempted during the season.
        """
        return int(self._opp_two_point_field_goal_attempts)

    @property
    def opp_two_point_field_goal_percentage(self):
        """
        Returns a float of the percentage of two point field goals made divided
        by the number of attempts by the opponent. Percentage ranges from 0-1.
        """
        return float(self._opp_two_point_field_goal_percentage)

    @property
    def opp_free_throws(self):
        """
        Returns an int of the total number of free throws made during the
        season by the opponent.
        """
        return int(self._opp_free_throws)

    @property
    def opp_free_throw_attempts(self):
        """
        Returns an int of the total number of free throw attempts during the
        season by the opponent.
        """
        return int(self._opp_free_throw_attempts)

    @property
    def opp_free_throw_percentage(self):
        """
        Returns a float of the percentage of free throws made divided by the
        attempts by the opponent. Percentage ranges from 0-1.
        """
        return float(self._opp_free_throw_percentage)

    @property
    def opp_offensive_rebounds(self):
        """
        Returns an int of the total number of offensive rebounds the opponent
        grabbed.
        """
        return int(self._opp_offensive_rebounds)

    @property
    def opp_defensive_rebounds(self):
        """
        Returns an int of the total number of defensive rebounds the opponent
        grabbed.
        """
        return int(self._opp_defensive_rebounds)

    @property
    def opp_total_rebounds(self):
        """
        Returns an int of the total number of rebounds the opponent grabbed.
        """
        return int(self._opp_total_rebounds)

    @property
    def opp_assists(self):
        """
        Returns an int of the total number of field goals that were assisted
        by the opponent.
        """
        return int(self._opp_assists)

    @property
    def opp_steals(self):
        """
        Returns an int of the total number of times the opponent stole the ball
        from the team.
        """
        return int(self._opp_steals)

    @property
    def opp_blocks(self):
        """
        Returns an int of the total number of times the opponent blocked the
        team's shot.
        """
        return int(self._opp_blocks)

    @property
    def opp_turnovers(self):
        """
        Returns an int of the total number of times the opponent turned the
        ball over.
        """
        return int(self._opp_turnovers)

    @property
    def opp_personal_fouls(self):
        """
        Returns an int of the total number of times the opponent fouled the
        team.
        """
        return int(self._opp_personal_fouls)

    @property
    def opp_points(self):
        """
        Returns an int of the total number of points the team has been scored
        on during the season.
        """
        return int(self._opp_points)


class Teams:
    """
    A list of all NBA teams and their stats in a given year.

    Finds and retrieves a list of all NBA teams from
    www.basketball-reference.com and creates a Team instance for every team
    that participated in the league in a given year. The Team class comprises
    a list of all major stats and a few identifiers for the requested season.
    """
    def __init__(self, year=None):
        """
        Get a list of all Team instances

        Once Teams is invoked, it retrieves a list of all NBA teams in the
        desired season and adds them to the '_teams' attribute.

        Parameters
        ----------
        year : string (optional)
            The requested year to pull stats from.
        """
        self._teams = []

        self._retrieve_all_teams(year)

    def __getitem__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        abbreviation.

        Parameters
        ----------
        abbreviation : string
            An NBA team's three letter abbreviation (ie. 'DET' for Detroit
            Pistons).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.

        Raises
        ------
        ValueError
            If the requested team is not present within the Teams list.
        """
        for team in self._teams:
            if team.abbreviation.upper() == abbreviation.upper():
                return team
        raise ValueError('Team abbreviation %s not found' % abbreviation)

    def __call__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        abbreviation. This method is a wrapper for __getitem__.

        Parameters
        ----------
        abbreviation : string
            An NBA team's three letter abbreviation (ie. 'DET' for Detroit
            Pistons).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.
        """
        return self.__getitem__(abbreviation)

    def __repr__(self):
        """Returns a list of all NBA teams for the given season."""
        return self._teams

    def __iter__(self):
        """Returns an iterator of all of the NBA teams for a given season."""
        return iter(self.__repr__())

    def __len__(self):
        """Returns the number of NBA teams for a given season."""
        return len(self.__repr__())

    def _add_stats_data(self, teams_list, team_data_dict):
        """
        Add a team's stats row to a dictionary.

        Pass table contents and a stats dictionary of all teams to accumulate
        all stats for each team in a single variable.

        Parameters
        ----------
        teams_list : generator
            A generator of all row items in a given table.
        team_data_dict : {str: {'data': str, 'rank': int}} dictionary
            A dictionary where every key is the team's abbreviation and every
            value is another dictionary with a 'data' key which contains the
            string version of the row data for the matched team, and a 'rank'
            key which is the rank of the team.

        Returns
        -------
        dictionary
            An updated version of the team_data_dict with the passed table row
            information included.
        """
        # Teams are listed in terms of rank with the first team being #1
        rank = 1
        for team_data in teams_list:
            abbr = utils._parse_field(PARSING_SCHEME,
                                      team_data,
                                      'abbreviation')
            try:
                team_data_dict[abbr]['data'] += team_data
            except KeyError:
                team_data_dict[abbr] = {'data': team_data, 'rank': rank}
            rank += 1
        return team_data_dict

    def _retrieve_all_teams(self, year):
        """
        Find and create Team instances for all teams in the given season.

        For a given season, parses the specified NBA stats table and finds all
        requested stats. Each team then has a Team instance created which
        includes all requested stats and a few identifiers, such as the team's
        name and abbreviation. All of the individual Team instances are added
        to a list.

        Note that this method is called directly once Teams is invoked and does
        not need to be called manually.

        Parameters
        ----------
        year : string
            The requested year to pull stats from.
        """
        team_data_dict = {}

        if not year:
            year = utils._find_year_for_season('nba')
        doc = pq(SEASON_PAGE_URL % year)
        teams_list = utils._get_stats_table(doc, 'div#all_team-stats-base')
        opp_teams_list = utils._get_stats_table(doc,
                                                'div#all_opponent-stats-base')
        for stats_list in [teams_list, opp_teams_list]:
            team_data_dict = self._add_stats_data(stats_list, team_data_dict)

        for team_data in team_data_dict.values():
            team = Team(team_data['data'], team_data['rank'], year)
            self._teams.append(team)
