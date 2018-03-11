#!/usr/bin/env python3
# encoding:utf-8

from lyftplan import *

johanna_2018_3_5 = Week([
Session("""
enbensmark  Växelvis arm/ben, sträck ut bak | 10 10 10
kb              Kontrollerat, korrekt stil! | 25x5 25x5 25x5 25x5

tryndrag                                    | 20 15 15
raka_latsdrag                               | 15 15 15
bp                                          | 40x8 40x8 45x4 45x4 50x2 50x2 60x1 60x1

sumomark                                    | 40x5 50x5 60x5 60x5 70x5 60x5
negativa_rh            Huvudet över stången | 1 1 1 1 1 1 1 1 1 1

kb              Kontrollerat, korrekt stil! | 25x5 25x5

militarpress                                | 20x8 20x8 20x8
latsdrag                                    | 20 15 10 10 10
tricepsrep                                  | 20 15 10 10 10
"""),
Session("""
tryndrag                                    | 20 15 15
sittande_rodd                       Kontakt | 15 15 15
bp                                          | 40x5 45x5 50x5 55x4 60x2 62.5x2 62.5x2
raka_latsdrag                       Kontakt | 10 15

enbensmark                                  | 10 10 10 10
sumomark                                    | 60x5 70x5 80x5 70x5 70x5

negativa_rh                                 | 1 1 1 1 1 1 1 1 1 1

kb                                          | 30x5 30x5 30x5 30x5 30x5 30x5 30x5 30x5
rygglyft                                    | 10 10
latsdrag                  Tungt med kontakt | 15 15 15 15
tricepsrep                                  | 15 15 15
"""),
Session("""
tryndrag                                    | 20 15 15
raka_latsdrag                       Kontakt | 15 15 15
sittande_rodd                       Kontakt | 15 15 15
negativa_rh                  Hela vägen ned | 1 1 1 1 1 1 1 1 1 1

enbensmark                                  | 10 10 10 10
kb_fram                                     | 30x5 35x5 40x5 45x5
kb                                          | 40x5 40x10 45x10

sumomark                                    | 55x5 65x5 75x5 75x5 75x5 75x5 75x5

pinpress                                    | 30x10 40x5 45x3 50x3 55x3 55x3 55x3

klotsving                                   | 16x20 20x20 24x20
tricepsrep                                  | 20 20 20 20 20
""", date=(2018,3,10))
]
)


johanna_2018_3_12 = Week([
Session("""
klotsving                                   | 16x20 20x15 24x10
negativa_rh Fokus varannan rep nere/uppe, 1 rep var 5-10 minut hela passet | 1
enbensmark  Växelvis arm/ben, sträck ut bak | 10 10 10
kb                                          | 20x10 30x10 40x5 45x5 50x5
kb_pin                                      | 30x4 35x4 40x4 45x4
raka_latsdrag                               | 15 15
bpfu                Lillfinger, stopp       | 30x5 40x5 50x3
bp                                          | 50x3 55x3 60x3 50x5 50x5
tryndrag                                    | 15 15 15
sumomark       Maxat grepp, inget bälte     | 40x5 50x5 60x5 70x5 80x1 80x1 80x1 80x1 80x1
sittande_rodd                   Kontakt     | 10 10 10 10 10
militarpress                                | 25x5 25x5 25x5
tricepsrep                                  | 20 15 10 10
"""),
]
)

cyberman_18_2 = Cycle([johanna_2018_3_5, johanna_2018_3_12], date=(2018,3,5))

current = cyberman_18_2

#
# App
#
def main():

    a = """
	   ╔Ω╗
	  [●_●]
	  ╔╠ ╣╗  C-Y-B-E-R-M-A-N 18.2
	  ╜╟ ╢╙
	   ╝ ╚"""

    a = """
                                   (&##%&%,                                  
                                *#  *#&&&&(. *&                                
            .................//#, @@@%, .,&@@. @*,,                            
       *@%*.,,              ., # (@@       /@& *( %               /../&&.      
      &(    ,,              ., / &@@       /@@ ./ %               /     %%     
     (#   .&(///////////////%%% ,@@@%     .@@@* %%&////////////////(&    &*    
     ##///&.               .#* *@@&(@.    ##%@@/ .%*                .#///%/    
     #*   #              %/  #@*%   *&   .&    %#&. .%*             .*   #/    
     #*   #            &, ,@*   &    &*  %/   ./   %%  (/           .*   #/    
     #*   #          *%  &,     &     (&&*    **     %#  %          .*   #/    
     #*   #        .%. %@@      #.            (.     /@@# ,#        .*   #/    
     #*   #       *( ,@@@@(     /*            %      @@@@@. (       .*   #/    
     #*   #   %&&&( /@./@@@     ,(            %     #@@@*.@% (%%%(  ,*   #/    
     #*   # (,(  / %@.  &@@/    .%            #     @@@#  ,@# *  (/.,*   #/    
     #*   #(. ( / /@(   (@@@     &           ,/    (@@@/   ,@, , ( ,(*   #/    
     #*   #&  ( , @&.   @@@@%    &           /,   ,@@@@&    @( ( (  @*   #/    
     &/...%@/ ( , @&   *@@/ .&,  (.          %.  #%  /@@,    ( ( #@/...%(    
     @    * %.( , @&   &@      ,#(*          &(%.      @%    ( (,(..   .&    
    (/    * %.( , @&  .@            ,/#%%#/,            @    ( (*(..    %,   
    ,&    * &.( , @&  **  (@@@@&                &@@@@(  *,   ( (*(..    @    
     ,@,  * &.( , @&  #  #@@@@@@@              @@@@@@@#  (  &% ( (*(..  *@.    
         .# &.( , @&  /  ,@@@@@@#              #@@@@@@,  (  && ( (*(.(,.       
           %% ( , @& .,  #,,##/                  *##,*#  (  && ( ( &/          
          ,&  ( , @&  (*                                //  && ( (  %          
          .@. ( , @%    ,&.                           %.    && ( ( ,#          
            @*( , @*     #%&,                       &%(     (& ( (((           
              /%* (      *& ,@.                   #( #,      ( ##*             
               .& (      .@                   .&   &       ( &               
                 #%       @    #@              *%    &       &/                
                  ,%.     &.   (@%            ,@#    %      &.                 
                    #*    #*   /@@*..........,@@/   .(    (&                   
                     ,%   *(   *@@#,,,,,,,,,.(@@*   /,   &,                    
                      %.  .%   .@@,          ,@@,   #   .&                     
                       ,&. &   .@@.           @@.   % ,@*                      
                          #&@,  @@            @@  .&&%                         
                             .@&            &@#&.                            
                                .,(%&@@@@@@@*.                               

	"""

    b = """
                    Exterminate!
                   /
              ___
      D>=G==='   '.
            |======|
            |======|
        )--/]IIIIII]
           |_______|
           C O O O D
          C O  O  O D
         C  O  O  O  D
         C__O__O__O__D
        [_____________] """



    print(a)

    print("""
====================================================
          S E S S I O N S
====================================================""")

    for i in range(len(current[0])):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPass {}: {}\n".format(i+1, current[0][i].date))
        print_session(current[0][i])
        print("------------------------------------")
        print_stats(Statistics(current[0][i]))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()

    print("""
====================================================
          T R A I N I N G   W E E K
====================================================""")
    for week in current.weeks:
        print("{}".format(week.date))
        print_stats(Statistics(week))
        print()

    print("""
====================================================
          T R A I N I N G   C Y C L E   {}
====================================================""".format(current.date))

    print_stats(Statistics(current), print_children=False)

    print("""
====================================================
          M A X   L I F T S
====================================================""")
    print_pr(Statistics(current))

    print("--------------------------------------------------------------------------------")
    #print_stats(Statistics(current[0][2]))


    #print("Pass C\n")
    #print_session(vecka[2], csv=True)

    import sys
    sys.exit(0)


    vecka = johanna_2018_3_5

    #print("Vecka 1: {}".format(vecka.date))
    print()


    for i in range(len(vecka)):
        print("Pass {}: {}".format(i+1, vecka[i].date))
        print_stats(Statistics(vecka[i]), indent=1)
        print()

    print("\nVecka:")
    print_stats(Statistics(vecka), indent=1)

    print("\n=======================================\n")

    for i in range(len(vecka)):
        print("Pass {}: {}".format(i+1, vecka[i].date))
        print_session(vecka[i])
        print()


    print("\nPass A:", vecka[0].date)
    print_session(vecka[0], csv=True)
    print("\nPass B:", vecka[1].date)
    print_session(vecka[1], csv=True)
    print("Pass C\n")
    print_session(vecka[2], csv=True)

    print("\nStatistik för vecka med start", vecka[0].date)
    stats = Statistics(vecka)
    print_stats(stats,csv=True)

    print()

    print_pr(stats)

if __name__ == '__main__':
    main()


