from decorators import benchmark
from math import sqrt

"""
# - BRICK
☼ - UNDESTROYABLE_WALL 

H - LADDER 
U - OTHER_HERO_LADDER
Y - HERO_LADDER
Q - ENEMY_LADDER 

~ - PIPE
Э - OTHER_HERO_PIPE_LEFT
Є - OTHER_HERO_PIPE_RIGHT
{ - HERO_PIPE_LEFT
} - HERO_PIPE_RIGHT
< - ENEMY_PIPE_LEFT
> - ENEMY_PIPE_RIGHT

ALL ANOTHER FOR THE FIRST TICK - EMPTY
"""


@benchmark
def main() -> None:
    map_string = 'board=☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼' \
                 '      (    ►                 ~~~~~~~~~     &     ~~~~~~~☼☼##H########################H#H' \
                 ' &    $H##########H       ☼☼  H         &  &&      &@  H######H (H        & H#☼☼☼☼☼#☼☼' \
                 'H☼☼#☼☼H &  H#########H   ( H#   $ H#####H#####H##&$~~~~~☼☼H     H    H   & && &H#####H#  ' \
                 '   H ~   H   &@H  ~~(((((☼☼H#☼#☼#H    H         H  ~~~&#####H#     H     H   $ЄЄ(((☼☼H@@~' \
                 '  H~~~~H~~~~~~   H        $  H$  H######H##    & ЄЄ(☼☼H     H& & H   $ H###☼☼☼☼☼☼H☼   &' \
                 'H~~~H    $ H( (     & #☼☼H     H    Q#####H     (  (H     H      H#########H     ☼☼☼###☼#' \
                 '#☼##☼H @& &  $ H###H##    H##     H#       ## ( ( ☼☼☼###☼~~~~& H         H $&H######H#####' \
                 '#### H###H #####H#☼☼☼(((☼  &   H   ~~~~~ЄH   H      H          H#@#H      H$☼☼########H###' \
                 '☼☼☼☼     H  ############   ######&##########☼☼        H           »Q       (  ($&         ' \
                 '      (  (  ☼☼H##########################H########Є~~####H############☼☼H                 ~' \
                 '~~ @$$  H              $H           &☼☼#######H#######  $@ @      H###~~~~     &############' \
                 'H &☼☼&  $&  H~~~~~~~~~~   (    »H                         H  ☼☼    &  H    ##H   #######Q####' \
                 '######~~~~~~~H######## H  ☼☼       H    ##H          H                 H   &&&   H  ☼☼##H#####' \
                 '    ########H#######~~~~  ~~~#########~~~~~  H  ☼☼  H                 H  & @$           &      ' \
                 '   $~~~~H  ☼☼#########H##########H  $ @   #☼☼☼☼☼☼#   ☼☼☼☼☼☼☼    $ H  ☼☼(  &&&&  H   $$   ' \
                 '  H        ~(( (((~            (   H  ☼☼☼☼       H~~~~~~~~~~H        &######   ###########   H' \
                 ' (☼☼    H###### $$&@ &  #######H    (      ~~~~~~~~~~~~~ЄH (☼☼H☼  H   (                  H ' \
                 ' H####H     »(          H (☼☼H☼☼#☼☼☼☼☼☼☼☼☼☼☼☼###☼☼☼☼☼☼☼☼H☼☼☼☼☼☼☼☼#☼☼☼☼☼☼☼☼☼☼☼☼' \
                 '☼☼☼☼☼☼#☼☼H @  &       ~~H~~~~☼☼☼☼☼☼☼H☼☼☼☼☼☼☼       H   ~~~~~~~~~H☼☼H~~~~  ######  H  ' \
                 '      $H☼H☼H        ####H (☼       & H☼☼H        &     ##H#######H☼H☼H######H &  $###☼☼☼☼☼☼' \
                 '☼☼ ~H☼☼H#########      (H    ~~~H☼H☼H~~~   H~~~~~&##(((((   ~ Q☼☼H && @  &###H## #H##H     ☼' \
                 'H☼@      H     ###☼☼☼☼☼☼ ~  H☼☼H        & &H   & &#######☼H☼#####  H##### & ~~~~~~~ ~ H☼☼~~~' \
                 '~~~~~~~~~H       H~~~~~☼H☼~~~~~  H       (  &&&~ ~  H☼☼ $   H              H((  (☼H☼     #####' \
                 '#####H (    (   Q☼☼ ### #############H H#####☼H☼   (       &   H ######## H☼☼H      & & $     ' \
                 ' H $   $$☼H☼####### &     (H          H☼☼H##### (   (  (H##H####      (         ###H######### ' \
                 '  H☼☼H   &  H######### H $ ############    «&  H            H☼☼H##    H    &     H~~~~~~     ' \
                 '            H #######H## H☼☼~~~~#####H#   ~~ЄЄH         ########H     H  &&$   H   H☼☼        ' \
                 ' H        H      ~~~~~~~~   H     H        H   H☼☼   ########H    ######H##   @    ##########' \
                 '####    H   H☼☼           H          H        ~Є~~~        $$ ##H#####H☼☼H    ###########H     ' \
                 'H#####H         H##H    &  H &   H☼☼H###            H     H     ###########$&##H###  H  (  H☼' \
                 '☼H  ######  ##H######  H                    H &$##H###  H☼☼H            H ~~~~~##H###H     ####' \
                 '#####H##        $  H☼☼    H########H#       H&  ######@        H  ((     &$  H☼☼ ###H        ' \
                 'H         ~~~~~H  &   ##H###H####H###     H☼☼    H########H######### &&  H        H &@     H' \
                 '        H☼☼H   H      @                Q(    (  H        H   (   @H☼☼H  ####H######         ' \
                 '#####H########H##      H#####   H☼☼H      H      H#######H        (              H     (  H☼☼#' \
                 '#############H       H#################################☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼' \
                 '☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼'.lstrip("board=")

    # Single coord = { (i, j): sign }
    # (0, 0), (0, board_side_length), (board_side_length, 0),
    #   (board_side_length, board_side_length) - unused (map edges)
    coords = {}

    board_cells_count = len(map_string)
    board_side_length = int(sqrt(board_cells_count))

    s = iter(map_string)
    for j in range(0, board_side_length):
        for i in range(0, board_side_length):
            coords[(i, j)] = next(s)

    edge = set()    # to save coordinates of one edge of a graph

    # Floor blocks list
    floor = []
    for y in range(1, board_side_length):
        for x in range(1, board_side_length):
            """
            Иф который во второй строке ниже (93)
            надо переписать с проверкой на не пустоту 
            для этого надо привести все символы которые не юзаются 
            в комменте наверху файла к одному 
            либо проверять каждый тип сверху но это чет пиздец
            """
            if (coords[(x, y)] != "#" and coords[(x, y)] != "☼") and \
                    (coords[(x, y + 1)] == "#" or coords[(x, y + 1)] == "☼"):  # вот всю эту строку
                edge.add((x, y))
            else:
                if len(edge) != 0:
                    floor.append(edge.copy())
                    edge.clear()
    print(floor)


if __name__ == '__main__':
    main()
