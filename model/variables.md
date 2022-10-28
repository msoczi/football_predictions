## Dataset description

Possible aggregation:
* avg - average
* std - standard deviation
* wz - coefficient of variation
* min - minimum
* max - maximum
* trd - trend (linear regression slope)

|     Variable    | Type        | Description                                                                                           |
|:---------------:|-------------|-------------------------------------------------------------------------------------------------------|
|       Date      | date        | match date                                                                                            |
|     HomeTeam    | string      | home team                                                                                             |
|     AwayTeam    | string      | away team                                                                                             |
|       FTR       | categorical | Full Time Result (H=Home Win, D=Draw, A=Away Win)                                                     |
|   h_pts_#AGG#N  | float       | aggregate of points scored by the home team in n matches                                              |
|   h_gz_#AGG#N   | float       | aggregate number of goals scored by the home team in n matches                                        |
|   h_gs_#AGG#N   | float       | aggregate number of goals conceded by the home team in n matches                                      |
|  h_sh_od_#AGG#N | float       | aggregate number of home team shots in n matches                                                      |
|  h_sh_ot_#AGG#N | float       | aggregate number of home team defended shots in n matches                                             |
| h_sot_od_#AGG#N | float       | aggregate number of home team shots on target in n matches                                            |
| h_sot_ot_#AGG#N | float       | aggregate number of home team defended shots on target in n matches                                   |
|   h_cw_#AGG#N   | float       | aggregate number of home team corners in the last n games                                             |
|   h_cb_#AGG#N   | float       | aggregate number of home team corners defended in the last n games                                    |
|   h_yc_#AGG#N   | float       | aggregate number of yellow cards for home team in the last n games                                    |
|   h_rc_#AGG#N   | float       | aggregate number of red cards for home team in the last n games                                       |
|  h_pts_per_math | float       | aggregate number of points from all games played so far in the current   season (home team)           |
|       h_gz      | float       | aggregate number of scored goals from all games played so far in the   current season (home team)     |
|       h_gs      | float       | aggregate number of conceded goals from all games played so far in the   current season (home team)   |
|     h_sh_od     | float       | aggregate number of shots from all games played so far in the current   season (home team)            |
|     h_sh_ot     | float       | aggregate number of shots conceded from all games played so far in the   current season (home team)   |
|       h_cw      | float       | aggregate number of corners from all games played so far in the current   season (home team)          |
|       h_cb      | float       | aggregate number of corners conceded from all games played so far in the   current season (home team) |
|    h_pozycja    | int         | the position of the home team in the league table                                                     |
|   a_pts_#AGG#N  | float       | aggregate of points scored by the away team in n matches                                              |
|   a_gz_#AGG#N   | float       | aggregate number of goals scored by the away team in n matches                                        |
|   a_gs_#AGG#N   | float       | aggregate number of goals conceded by the away team in n matches                                      |
|  a_sh_od_#AGG#N | float       | aggregate number of away team shots in n matches                                                      |
|  a_sh_ot_#AGG#N | float       | aggregate number of away team defended shots in n matches                                             |
| a_sot_od_#AGG#N | float       | aggregate number of away team shots on target in n matches                                            |
| a_sot_ot_#AGG#N | float       | aggregate number of away team defended shots on target in n matches                                   |
|   a_cw_#AGG#N   | float       | aggregate number of away team corners in the last n games                                             |
|   a_cb_#AGG#N   | float       | aggregate number of away team corners defended in the last n games                                    |
|   a_yc_#AGG#N   | float       | aggregate number of yellow cards for away team in the last n games                                    |
|   a_rc_#AGG#N   | float       | aggregate number of red cards for away team in the last n games                                       |
|  a_pts_per_math | float       | aggregate number of points from all games played so far in the current   season (away team)           |
|       a_gz      | float       | aggregate number of scored goals from all games played so far in the   current season (away team)     |
|       a_gs      | float       | aggregate number of conceded goals from all games played so far in the   current season (away team)   |
|     a_sh_od     | float       | aggregate number of shots from all games played so far in the current   season (away team)            |
|     a_sh_ot     | float       | aggregate number of shots conceded from all games played so far in the   current season (away team)   |
|       a_cw      | float       | aggregate number of corners from all games played so far in the current   season (away team)          |
|       a_cb      | float       | aggregate number of corners conceded from all games played so far in the   current season (away team) |
|    a_pozycja    | int         | the position of the away team in the league table                                                     |
|   position_dst  | int         | position difference in the table                                                                      |
|      h_ATT      | int         | home team attack rating                                                                               |
|      h_MID      | int         | home team midfield rating                                                                             |
|      h_DEF      | int         | home team defense rating                                                                              |
|      h_OVR      | int         | home team overall rating                                                                              |
|      a_ATT      | int         | away team attack rating                                                                               |
|      a_MID      | int         | away team midfield rating                                                                             |
|      a_DEF      | int         | away team defense rating                                                                              |
|      a_OVR      | int         | away team overall rating                                                                              |
|     ATT_dst     | int         | difference in attack rating                                                                           |
|     MID_dst     | int         | difference in midfield rating                                                                           |
|     DEF_dst     | int         | difference in defense rating                                                                           |
|     OVR_dst     | int         | difference in overall rating                                                                           |

