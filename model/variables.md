## Dataset description

| Variable       | Type        | Description                                                                                         |
|:--------------:|:------------|:----------------------------------------------------------------------------------------------------|
| Date           | date        | match date                                                                                          |
| HomeTeam       | string      | home team                                                                                           |
| AwayTeam       | string      | away team                                                                                           |
| FTR            | categorical | Full Time Result (H=Home Win, D=Draw, A=Away Win)                                                   |
| h_course       | float       | home win odds                                                                                       |
| d_course       | float       | draw win odds                                                                                       |
| a_course       | float       | away win odds                                                                                       |
| h_pts_n        | float       | average of points scored by the home team in n matches                                              |
| h_gz_n         | float       | average number of goals scored by the home team in n matches                                        |
| h_gs_n         | float       | average number of goals conceded by the home team in n matches                                      |
| h_sh_od_n      | float       | average number of home team shots in n matches                                                      |
| h_sh_ot_n      | float       | average number of home team defended shots in n matches                                             |
| h_sot_od_n     | float       | average number of home team shots on target in n matches                                            |
| h_sot_ot_n     | float       | average number of home team defended shots on target in n matches                                   |
| h_cw_n         | float       | average number of home team corners in the last n games                                             |
| h_cb_n         | float       | average number of home team corners defended in the last n games                                    |
| h_yc_n         | float       | average number of yellow cards for home team in the last n games                                    |
| h_rc_3         | float       | average number of red cards for home team in the last n games                                       |
| h_pts_per_math | float       | average number of points from all games played so far in the current   season (home team)           |
| h_gz           | float       | average number of scored goals from all games played so far in the   current season (home team)     |
| h_gs           | float       | average number of conceded goals from all games played so far in the   current season (home team)   |
| h_sh_od        | float       | average number of shots from all games played so far in the current   season (home team)            |
| h_sh_ot        | float       | average number of shots conceded from all games played so far in the   current season (home team)   |
| h_cw           | float       | average number of corners from all games played so far in the current   season (home team)          |
| h_cb           | float       | average number of corners conceded from all games played so far in the   current season (home team) |
| h_pozycja      | int         | the position of the home team in the league table                                                   |
| a_pts_n        | float       | average of points scored by the away team in n matches                                              |
| a_gz_n         | float       | average number of goals scored by the away team in n matches                                        |
| a_gs_n         | float       | average number of goals conceded by the away team in n matches                                      |
| a_sh_od_n      | float       | average number of away team shots in n matches                                                      |
| a_sh_ot_n      | float       | average number of away team defended shots in n matches                                             |
| a_sot_od_n     | float       | average number of away team shots on target in n matches                                            |
| a_sot_ot_n     | float       | average number of away team defended shots on target in n matches                                   |
| a_cw_n         | float       | average number of away team corners in the last n games                                             |
| a_cb_n         | float       | average number of away team corners defended in the last n games                                    |
| a_yc_n         | float       | Average number of yellow cards for away team in the last n games                                    |
| a_rc_3         | float       | Average number of red cards for away team in the last n games                                       |
| a_pts_per_math | float       | average number of points from all games played so far in the current   season (away team)           |
| a_gz           | float       | average number of scored goals from all games played so far in the   current season (away team)     |
| a_gs           | float       | average number of conceded goals from all games played so far in the   current season (away team)   |
| a_sh_od        | float       | average number of shots from all games played so far in the current   season (away team)            |
| a_sh_ot        | float       | average number of shots conceded from all games played so far in the   current season (away team)   |
| a_cw           | float       | average number of corners from all games played so far in the current   season (away team)          |
| a_cb           | float       | average number of corners conceded from all games played so far in the   current season (away team) |
| a_pozycja      | int         | the position of the away team in the league table                                                   |
| position_dst   | int         | position difference in the table                                                                    |