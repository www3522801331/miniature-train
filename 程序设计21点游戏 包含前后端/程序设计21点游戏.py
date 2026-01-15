import random  # 随机顺序模块
from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


class Card:
    def __init__(self, suit, rank):
        self.suit = suit  # 花色
        self.rank = rank  # 牌面

    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        return f'{self.suit}{self.rank}'

    def to_dict(self):  # 转成字典（方便前端接收）
        return {"suit": self.suit, "rank": self.rank, "value": self.get_value()}


class Deck:
    def __init__(self):
        suits = ["♠️", "♥️", "♦️", "♣️"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        """洗牌：打乱牌堆顺序"""
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None


class Player:
    def __init__(self, name):
        self.name = name  # 玩家名字
        self.hand = []  # 手牌列表（存Card对象）
        self.is_bust = False  # 新增：标记是否爆牌（解决player_hit报错）

    def add_card(self, card):
        """添加一张牌到手牌"""
        self.hand.append(card)
        # 加牌后自动检查是否爆牌
        self.is_bust = self.calculate_hand() > 21

    def calculate_hand(self):
        """计算手牌总点数（自动处理A的11/1转换）"""
        total = 0
        ace_count = 0  # 统计A的数量（用于后续转换）

        # 第一步：先按A=11计算总点数
        for card in self.hand:
            val = card.get_value()
            total += val
            if val == 11:  # 只要是A，就计数
                ace_count += 1

        # 第二步：如果总点数>21，把A从11转成1（每次减10）
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1
        return total

    def is_blackjack(self):
        return len(self.hand) == 2 and self.calculate_hand() == 21

    def to_dict(self):  # 转字典给前端
        return {
            "name": self.name,
            "hand": [card.to_dict() for card in self.hand],
            "total": self.calculate_hand(),
            "is_bust": self.is_bust  # 新增：爆牌状态传给前端
        }


class Dealer(Player):
    def __init__(self, name="庄家"):
        super().__init__(name)

    def should_hit(self):
        return self.calculate_hand() < 17

# ========== 核心修改1：统一键名 current_player_id ==========
game_state = {
    "deck": None,
    "players": [],  # 多玩家列表
    "dealer": None,  # 庄家
    "game_over": False,  # 判断游戏是否结束
    "result": "",  # 游戏结果
    "stand_players": set(),  # 已停牌的玩家ID集合
    "current_player_id": 0  # 修正：键名统一为current_player_id
}


# 4. 定义API接口：初始化游戏（支持多玩家）
@app.route('/api/init_game', methods=['POST'])
def init_game():
    req_data = request.get_json() or {}
    player_count = req_data.get("player_count", 2)
    if not (1 <= player_count <= 4):
        return jsonify({"error": "玩家数量需在1-4人之间"}), 400

    # 重置游戏状态
    game_state["deck"] = Deck()
    game_state["players"] = [Player(f"玩家{i+1}") for i in range(player_count)]  # 多玩家初始化
    game_state["dealer"] = Dealer()
    game_state["game_over"] = False
    game_state["result"] = ""
    game_state["stand_players"] = set()  # 清空已停牌玩家
    game_state["current_player_id"] = 0  # 修正：使用统一的键名

    # 发初始牌：每个玩家+庄家各发1张
    for _ in range(1):
        for player in game_state["players"]:
            player.add_card(game_state["deck"].deal_card())
        game_state["dealer"].add_card(game_state["deck"].deal_card())

    # 返回当前游戏状态给前端（适配多玩家）
    return jsonify({
        "players": [p.to_dict() for p in game_state["players"]],
        "dealer": game_state["dealer"].to_dict(),
        "game_over": game_state["game_over"],
        "result": game_state["result"],
        "current_player_id": game_state["current_player_id"]  # 修正：取值键名匹配
    })


# 5. 定义API接口：玩家抽牌（适配多玩家）
@app.route('/api/player_hit', methods=['POST'])
def player_hit():
    if game_state["game_over"]:
        return jsonify({"error": "游戏已结束，请重新开始"}), 400

    req_data = request.get_json() or {}
    player_id = req_data.get("player_id", 0)
    current_player_id = game_state["current_player_id"]

    if player_id != current_player_id:
        return jsonify({"error": f"请先完成{game_state['players'][current_player_id].name}的操作！"}), 400

    player = game_state["players"][player_id]
    if player.is_bust:
        return jsonify({"error": f"{player.name}已爆牌，无法抽牌"}), 400

    new_card = game_state["deck"].deal_card()
    if not new_card:
        return jsonify({"error": "牌堆已空"}), 400
    player.add_card(new_card)

    result = ""
    # 判定状态并初始化提示
    if player.is_blackjack():
        base_tip = "拿到Blackjack"
        game_state["stand_players"].add(player_id)
    elif player.calculate_hand() == 21:
        base_tip = "拿到21点"
        game_state["stand_players"].add(player_id)
    elif player.is_bust:
        base_tip = "爆牌"
        game_state["stand_players"].add(player_id)
    else:
        result = f"{player.name}抽牌，当前点数：{player.calculate_hand()}"
        # 未完成操作，直接返回
        return jsonify({
            "players": [p.to_dict() for p in game_state["players"]],
            "dealer": game_state["dealer"].to_dict(),
            "game_over": game_state["game_over"],
            "result": result,
            "current_player_id": game_state["current_player_id"]
        })

    # 核心修改：根据是否有下一位玩家调整提示语
    next_player_id = current_player_id + 1
    if player_id in game_state["stand_players"]:
        if next_player_id < len(game_state["players"]):
            game_state["current_player_id"] = next_player_id
            result = f"{player.name}{base_tip}！自动切换到下一位玩家"
        else:
            # 无下一位玩家，提示“触发庄家回合”并执行
            result = f"{player.name}{base_tip}！所有玩家操作完成，即将触发庄家回合"
            time.sleep(2)
            dealer_turn()
            determine_winner()
            # 覆盖为最终胜负结果
            result = game_state["result"]

    return jsonify({
        "players": [p.to_dict() for p in game_state["players"]],
        "dealer": game_state["dealer"].to_dict(),
        "game_over": game_state["game_over"],
        "result": result,
        "current_player_id": game_state["current_player_id"]
    })

@app.route('/api/player_stand', methods=['POST'])
def player_stand():
    if game_state["game_over"]:
        return jsonify({"error": "游戏已结束，请重新开始"}), 400

    # 获取请求中的玩家ID
    req_data = request.get_json() or {}
    player_id = req_data.get("player_id", 0)
    current_player_id = game_state["current_player_id"]  # 修正：键名匹配
    # 限制：只能操作当前轮次的玩家
    if player_id != current_player_id:
        return jsonify({"error": f"请先完成{game_state['players'][current_player_id].name}的操作！"}), 400

    # 标记当前玩家停牌
    game_state["stand_players"].add(player_id)
    player = game_state["players"][player_id]
    result = f"{player.name}选择停牌，切换到下一位玩家"

    # 切换到下一位玩家
    next_player_id = current_player_id + 1
    if next_player_id < len(game_state["players"]):
        game_state["current_player_id"] = next_player_id  # 修正：键名匹配
    else:
        # 所有玩家完成，触发庄家回合
        time.sleep(2)
        dealer_turn()
        determine_winner()
        result = game_state["result"]

    return jsonify({
        "players": [p.to_dict() for p in game_state["players"]],
        "dealer": game_state["dealer"].to_dict(),
        "game_over": game_state["game_over"],
        "result": result,
        "current_player_id": game_state["current_player_id"]
    })

# 庄家回合：抽牌直到≥17，每抽一张停顿1秒（修正缩进+延迟）
def dealer_turn():
    dealer = game_state["dealer"]
    deck = game_state["deck"]
    print("庄家开始抽牌...")

    # 庄家抽牌（每抽一张停顿1秒，优化体验）
    while dealer.should_hit():
        new_card = deck.deal_card()
        if not new_card:
            break
        dealer.add_card(new_card)
        print(f"庄家抽到：{new_card}，当前点数：{dealer.calculate_hand()}")
        time.sleep(1)  # 修正：抽牌间隔1秒（原2秒不符合需求）

    # 检查庄家是否爆牌
    if dealer.calculate_hand() > 21:
        game_state["result"] = "庄家爆牌！"

# 判定多玩家胜负
def determine_winner():
    if game_state["game_over"]:
        return

    dealer = game_state["dealer"]
    dealer_total = dealer.calculate_hand()
    dealer_blackjack = dealer.is_blackjack()
    player_results = []

    # 逐个判定玩家胜负
    for player in game_state["players"]:
        player_total = player.calculate_hand()
        player_blackjack = player.is_blackjack()

        if player.is_bust:
            player_results.append(f"{player.name}：已爆牌，失败")
        elif dealer_total > 21:
            player_results.append(f"{player.name}：庄家爆牌，获胜")
        elif player_blackjack and not dealer_blackjack:
            player_results.append(f"{player.name}：Blackjack，获胜")
        elif dealer_blackjack and not player_blackjack:
            player_results.append(f"{player.name}：庄家Blackjack，失败")
        elif player_total > dealer_total:
            player_results.append(f"{player.name}：{player_total} > {dealer_total}，获胜")
        elif player_total < dealer_total:
            player_results.append(f"{player.name}：{player_total} < {dealer_total}，失败")
        else:
            player_results.append(f"{player.name}：{player_total} = {dealer_total}，平局")

    # 汇总结果
    game_state["result"] = "\n".join(player_results)
    game_state["game_over"] = True

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)