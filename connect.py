import websocket

from funcs import new_msg

websocket.default_timeout = 3600


class GameClient:
    def __init__(self, url):
        path = url.replace("http", "ws")
        path = path.replace("board/player/", "ws?user=")
        path = path.replace("?code=", "&code=")

        self.socket = websocket.WebSocketApp(
            path,
            on_message=lambda ws, msg: self._on_message(ws, msg),
            on_error=lambda ws, err: self._on_error(ws, err),
            on_close=lambda ws, err: self._on_close(ws),
            on_open=lambda ws, err: self._on_open(ws)
        )
        self.socket.run_forever()

    def _on_message(self, ws, message):
        map_str = message.lstrip("board=")
        action = new_msg(map_str)
        self.__send(action)

    def __send(self, msg):
        self.socket.send(msg)

    @staticmethod
    def _on_error(ws, error):
        print(f'Something was wrong!\n{error}')

    @staticmethod
    def _on_open(ws):
        print(f'Connection successfully established! {ws}')

    @staticmethod
    def _on_close(ws):
        print(f'Connection closed! {ws}')


# to tests
base_map_string1 = 'board=☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼' \
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
             '☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼'
base_map_string2 = 'board=☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼                    $  $     ' \
                  '~~~~~~~~~     @     ~~~~~~~☼☼##H########################H#H &    $H##########H       ' \
                  '☼☼$ H         ' \
                  '      (        H######H& H          H#☼☼☼☼☼#☼☼H☼☼#☼☼H   @H#########H     H#     H##' \
                  '###H#####H##  ' \
                  '~~~~~☼☼H&  & H    H         H#####H#     H ~   H  &  H  ~~ $  $☼☼H#☼#☼#H    H       &' \
                  ' H& ~~~ ' \
                  '#####H#@ $  H   @ H    ~~   ☼☼H  ~ $H~~~~H~~~~~~   H   @     @ H   H######H##      ~~ ' \
                  '☼☼H     H    ' \
                  'H$    H###☼☼☼☼☼☼H☼    H~~~H      H     &    #☼☼H     H    H#####H         H  $& H   ' \
                  '   H#########H ' \
                  '    ☼☼H###☼##☼##☼H         H###H##    H##  $  H# $   &$##   @ ☼☼H###☼~~~~ &H       ' \
                  '  H   ' \
                  'H######H######### H###H #####H#☼☼H     $    H   ~~~~~~H   H     &H          H# #H      ' \
                  'H ' \
                  '☼☼########H###☼☼☼☼     H$ ############   ###### ##########☼☼       @H            H  ' \
                  '      $        ' \
                  '           $  &  ☼☼H##########################H########Є~~####H############☼☼H       ' \
                  '          ~~~ ' \
                  '     H  $            H    &       ☼☼#######H####### &         «H###~~~~      ##########' \
                  '##H  ☼☼  @  ' \
                  '  H~~~~~~~~~~  $ ((   H«    &           (       H  ☼☼     &&H    ##H   ' \
                  '#######H##########~~~~~~~H######## H  ☼☼   (   H    ##H          H        &&   & $ H  ' \
                  '       H ' \
                  '&☼☼##H#####  & ########H#######~~~~  ~~~#########~~~~~  H  ☼☼  H            &    H   ' \
                  '           ( ' \
                  '&$  &       ~~~~H  ☼☼#########H##########H      &&#☼☼☼☼☼☼#   ☼☼☼☼☼☼☼      H  ☼☼ ' \
                  '   &    H         ' \
                  '&H   $    ~      ~                H  ☼☼☼☼   (   H~~~~~~~~~~H      (« ######   ######' \
                  '#####   H&&☼☼ ' \
                  '@  H######  &   $  #######H         & ~~~~~~~~~~~~~~H  ☼☼H☼  H          &      @    H&' \
                  ' H####H      ' \
                  '   @       H  ☼☼H☼☼#☼☼☼☼☼☼☼☼☼☼☼☼###☼☼☼☼☼☼☼☼H☼☼☼☼☼☼☼☼#☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼' \
                  '☼☼#☼☼H           (' \
                  '~~H~~~~☼☼☼☼☼☼☼H☼☼☼☼☼☼☼       H   ~~~~~~~~~H☼☼H~~~~  ######  H         H☼H☼H&     ' \
                  '  ####H  ☼        ' \
                  '&H☼☼H        &     ##H#######H☼H☼H######H &   ###☼☼☼☼☼☼☼☼ ~H☼☼H#########  &    H ' \
                  '$  ~~~H☼H☼H~~~   ' \
                  'H~~~~~ ##   (    ~ H☼☼H        ###H####H##H&    ☼H☼       H     ###☼☼☼☼☼☼ ~  H☼☼H' \
                  '           H      ' \
                  '#######☼H☼#####  H#####$  ~~~~~~~ ~&H☼☼~~~~~~~~~~~~H       H~~~~~☼H☼~~~~~  H        ' \
                  '     ~ ~  H☼☼  ' \
                  '   H  &         & H    $☼H☼$    ##########H  @    @  H☼☼ ### #############H H#####☼H' \
                  '☼              ' \
                  ' H ######## H☼☼H$  ( $        & (H    $  ☼H☼#######        H          H☼☼H#####      ' \
                  ' & H##H####&& ' \
                  '             ###H#########   H☼☼H$     H######### H  &############ &$&@   H           ' \
                  ' H☼☼H##    H ' \
                  '         H~~~~~~        »        H #######H## H☼☼~~~~#####H#   ~~~~H  &      ########H' \
                  '    &H      ' \
                  '& H   H☼☼ $$   &  H   @    H      ~~~~~~~~   H@ &(&H&  &    H   H☼☼   ########H    ##' \
                  '####H##       ' \
                  ' ##############    H (&H☼☼        &  H          H    &  &~~~~~$        &&##H#####H☼☼H    ' \
                  '###########H     H#####H         H##H      &H     H☼☼H###   »        H     H  @  #####' \
                  '###### ' \
                  '&##H###& H     H☼☼H @######  ##H######  H   $                H   ##H###  H☼☼H            H ' \
                  '~~~~~##H###H    )#########H##           H☼☼    H########H# $     H   ######         H  ' \
                  '           ' \
                  'H☼☼ ###H     $ &H $   @   ~~~~~H      ##H###H####H###     H☼☼   &H########H#########    ' \
                  '&H        ' \
                  'H        H        H☼☼H   H  &&              &    H&   ►   H   $    H   (    H☼☼H  ####' \
                  'H######     ' \
                  '&   #####H########H##      H#####   H☼☼H      H      H#######H        &    &         H' \
                  '    &   ' \
                  'H☼☼##############H       ' \
                  'H#################################☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼' \
                  '☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼ '
