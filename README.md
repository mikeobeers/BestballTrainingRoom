# Bestball Training Room
This is an application developed to help bestball players practice roster construciton across various league formats on their own time, against realistic AI opponents. The application makes use of the 'pygame' library, and the script which launches the game can be found in draftgame2021.py. The accompanying scripts and 'data' folder are dependencies of the main file, and must be saved in the same directory for the program to run.

Upon running draftgame2021.py, a window will launch and the user will be prompted to select a format for their draft.  You may select from a number of common bestball draft formats, mimicing the rules and scoring from popular platforms including bestball10s (BB10), FFPC, Underdog (UD) and DraftKings (DK).

![Format Selection](https://user-images.githubusercontent.com/32966273/133839547-9ab6a407-9cfa-4106-8a96-82fc0b018f90.png)

After clicking on the desired format, clicking the 'Start' button will launch the game.  A draft grid will appear, with the number of teams and rounds corresponding to the selected format, and the user will be assigned a random draft position, highlighted in yellow.  The game will also randomly assign a "Draft Season" of "Feb-Apr," "May-Jul" or "Aug-Sep" for the draft.  The game will references the draft season when assigning players to each team at the end of the draft.

When the user's team is "on the clock," buttons will appear above the draft grid allowing the user to select a player.  Because the purpose of this game is to practice roster construction, they are not selecting specific players, but instead are picking by position (e.g. if 4 running backs have already been selected, the user will have the option of selecting "RB5").  At the conclusion of the draft, the actual player name and statistics for the player with the corresponding Average Draft Position (ADP) from a randomly selected year between 2015-2020 and the given "draft season" (e.g. Feb-Apr 2017).

Picks for opposing teams are made using a decision tree algorithm generated from analysis of over 1-million actual bestball teams drafted over the past 6 years. The opponent AI algorithm is designed to mimic realistic drafters, as opposed to "optimized" drafters.

![GameStart](https://user-images.githubusercontent.com/32966273/133840245-ea2fa59a-1eb5-4e3e-9760-75030405b3ca.png)

At the conclusion of the draft, the program assigns players to each team using the above methodology, and calculates weekly, and full season scores for each team based on how those players actually performed in the given year.  Those scores are used to generate a standings table which appears below the draft grid. The player names used to generate the scores are also filled into the draft grid and the "Roster Table" once the scores have been generated, allowing the user to see who they would have drafted, according to ADP.  This process allows users to practice different roster constructions and see how they may have faired across time.

![Completed Draft](https://user-images.githubusercontent.com/32966273/133842089-7cfec805-7c48-4fbe-834e-e0fb1565eb48.png)
