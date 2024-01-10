from flask import *
import datetime
import time
import poker
import rank
import rounds

app = Flask(__name__)
app.secret_key = "9d263e09465118fcc3b288369ed53396922588fc3e8f466845ef8ab6a00cef25"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hall")
def hall():
    date_heure = datetime.datetime.now()
    h = date_heure.hour
    m = date_heure.minute
    s = date_heure.second
    return render_template("hall.html", heure=h, minute=m, seconde=s)


@app.route("/hall/game__off")
def game__of():
    deck = poker.generate_deck()
    hands = poker.deal_hand(deck, 5)
    river = poker.River(deck) 
    best = poker.Best_hand(hands,river)
    winrank = rank.evaluate_hand(rank.get_best_hand(hands[best[0]]+river))
    return render_template("game__off.html", hands=hands, nbp = len(hands), river=river , winner=best, winrank = winrank)

POT = 0
FOLDED = []
IN_GAME = ["admin"]
IN_WAIT = []
utilisateurs = [
        {"nom": "admin", "mdp": "1234", "money": 500},
        {"nom": "marie", "mdp": "nsi", "money": 500},
        {"nom": "paul", "mdp": "azerty", "money": 500}  
]
actual_player = "admin"
it_is_running = True
min_bet = 0

def recherche_utilisateur(user_name, mot_de_passe):
    for utilisateur in utilisateurs:
        if utilisateur['nom'] == user_name and utilisateur['mdp'] == mot_de_passe:
            return utilisateur
    return None

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')

        utilisateur = recherche_utilisateur(nom, mdp)

        if utilisateur is not None:
            print("utilisateur trouvé")
            session['user_name'] = utilisateur['nom']
            session['money'] = utilisateur['money']
            print(session)
            return redirect(url_for('index'))
        else:
            print("utilisateur inconnu")
            return redirect(request.url)
    else:
        print(session)
        if 'user_name' in session:
            return redirect(url_for('index'))
        return render_template("login.html")

@app.route('/logout')
def logout():
    print(session)
    session.pop('user_name', None)
    session.pop('money', None)
    print(session)
    return redirect(url_for('login'))


@app.route("/hall/game", methods=["GET", "POST"])
def game():
    if request.method == "GET":
        ifexit = request.args.get('exit')
        if ifexit == 'QUITTER':
            rounds.QUIT_GAME(session['user_name'], IN_GAME, IN_WAIT)
            return redirect(url_for('index'))
    
    if 'user_name' in session:
        if rounds.gotoIN_WAIT(session, IN_GAME, IN_WAIT):
            IN_WAIT.append(session['user_name'])
        if len(IN_WAIT) >= 2:
            if actual_player == session['user_name']:
                donne = request.form
                move = donne.get('move')
                moved = make_move(move, bet, session['money'], POT)
                if moved is not None:
                    if moved == 'FOLD':
                        IN_GAME.pop(IN_GAME[IN_GAME.index(actual_player)])
                    if IN_GAME.index(actual_player) + 1 == len(IN_GAME):
                        actual_player = IN_GAME[0]
                    else:
                        actual_player = IN_GAME[IN_GAME.index(actual_player) + 1]
        return render_template("game.html", IN_WAIT=IN_WAIT, IN_GAME=IN_GAME, disp_inp=(actual_player == session['user_name']))
    return redirect(url_for('login'))


def make_move(move, bet, money, min_bet, POT):
    if move is not None:
        if move == 'FOLD':
            return 'FOLD'
        elif move == 'RAISE':
            bet = int(donne.get('bet'))
            money -= bet 
            POT += bet
            min_bet = bet
        elif move == 'ALL-IN':
            if min_bet < money:
                min_bet = money
            POT += money
            money = 0
        elif move == 'CHECK':
            money -= min_bet
            POT += min_bet
        return [POT, money, min_bet]
    return None

def next_player(IN_GAME, actual_player)
    if IN_GAME.index(actual_player) + 1 == len(IN_GAME):
        actual_player = IN_GAME[0]
    else:
        actual_player = IN_GAME[IN_GAME.index(actual_player) + 1]

if __name__ == '__main__':
    app.run(debug=True)
