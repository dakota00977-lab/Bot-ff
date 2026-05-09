import discord
from discord.ext import commands
import json
import os

# Configurações básicas
TOKEN = 'SEU_TOKEN_AQUI' # O usuário deverá substituir pelo seu token
DB_FILE = 'database.json'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Banco de dados simples em JSON
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "matches": {}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='cadastro')
async def register(ctx):
    """Cadastra o jogador com um saldo inicial de 1000 moedas."""
    db = load_db()
    user_id = str(ctx.author.id)
    
    if user_id in db['users']:
        await ctx.send(f'{ctx.author.mention}, você já está cadastrado!')
    else:
        db['users'][user_id] = {
            "name": ctx.author.name,
            "balance": 1000,
            "wins": 0
        }
        save_db(db)
        await ctx.send(f'Bem-vindo ao FF Bet, {ctx.author.mention}! Você recebeu 1000 moedas iniciais.')

@bot.command(name='saldo')
async def balance(ctx):
    """Consulta o saldo atual do jogador."""
    db = load_db()
    user_id = str(ctx.author.id)
    
    if user_id not in db['users']:
        await ctx.send(f'{ctx.author.mention}, use `!cadastro` primeiro.')
    else:
        balance = db['users'][user_id]['balance']
        await ctx.send(f'{ctx.author.mention}, seu saldo atual é de **{balance} moedas**.')

@bot.command(name='criar_partida')
@commands.has_permissions(administrator=True)
async def create_match(ctx, match_id: str, entry_fee: int, description: str):
    """Cria uma nova partida de aposta (Apenas Admins)."""
    db = load_db()
    
    if match_id in db['matches']:
        await ctx.send('Uma partida com esse ID já existe.')
        return
        
    db['matches'][match_id] = {
        "entry_fee": entry_fee,
        "description": description,
        "players": [],
        "status": "open"
    }
    save_db(db)
    await ctx.send(f'Partida **{match_id}** criada! \nTaxa de entrada: **{entry_fee}** \nDescrição: {description} \nUse `!apostar {match_id}` para entrar.')

@bot.command(name='apostar')
async def bet(ctx, match_id: str):
    """Entra em uma partida de aposta."""
    db = load_db()
    user_id = str(ctx.author.id)
    
    if user_id not in db['users']:
        await ctx.send(f'{ctx.author.mention}, use `!cadastro` primeiro.')
        return
        
    if match_id not in db['matches']:
        await ctx.send('Partida não encontrada.')
        return
        
    match = db['matches'][match_id]
    if match['status'] != 'open':
        await ctx.send('As apostas para esta partida já estão fechadas.')
        return
        
    if user_id in match['players']:
        await ctx.send('Você já está nesta partida.')
        return
        
    entry_fee = match['entry_fee']
    if db['users'][user_id]['balance'] < entry_fee:
        await ctx.send('Você não tem saldo suficiente.')
        return
        
    # Deduz o saldo e adiciona o jogador
    db['users'][user_id]['balance'] -= entry_fee
    match['players'].append(user_id)
    save_db(db)
    
    await ctx.send(f'{ctx.author.mention} entrou na partida **{match_id}**! Boa sorte!')

@bot.command(name='vencedor')
@commands.has_permissions(administrator=True)
async def set_winner(ctx, match_id: str, winner: discord.Member):
    """Define o vencedor de uma partida e distribui o prêmio (Apenas Admins)."""
    db = load_db()
    
    if match_id not in db['matches']:
        await ctx.send('Partida não encontrada.')
        return
        
    match = db['matches'][match_id]
    winner_id = str(winner.id)
    
    if winner_id not in match['players']:
        await ctx.send('O vencedor indicado não estava na partida.')
        return
        
    # Calcula o prêmio total (pode ser ajustado para tirar uma taxa da casa)
    total_pool = len(match['players']) * match['entry_fee']
    
    db['users'][winner_id]['balance'] += total_pool
    db['users'][winner_id]['wins'] += 1
    match['status'] = 'finished'
    match['winner'] = winner_id
    
    save_db(db)
    await ctx.send(f'🏆 **Parabéns {winner.mention}!** Você venceu a partida **{match_id}** e ganhou **{total_pool} moedas**!')

@bot.command(name='ranking')
async def leaderboard(ctx):
    """Mostra o ranking dos jogadores com mais moedas."""
    db = load_db()
    users = db['users']
    
    sorted_users = sorted(users.items(), key=lambda x: x[1]['balance'], reverse=True)[:5]
    
    leaderboard_str = "**🏆 Ranking Top 5 - FF Bet**\n"
    for i, (uid, data) in enumerate(sorted_users, 1):
        leaderboard_str += f"{i}. {data['name']} - {data['balance']} moedas\n"
        
    await ctx.send(leaderboard_str)

@bot.command(name='ajuda_ff')
async def help_command(ctx):
    """Mostra os comandos disponíveis."""
    help_text = """
**Comandos do FF Bet Bot:**
`!cadastro` - Cria sua conta com 1000 moedas iniciais.
`!saldo` - Veja quantas moedas você tem.
`!apostar <id_partida>` - Entra em uma partida aberta.
`!ranking` - Veja os jogadores mais ricos.
`!ajuda_ff` - Mostra esta mensagem.

**Comandos de Admin:**
`!criar_partida <id> <taxa> <descrição>` - Cria uma nova partida.
`!vencedor <id_partida> @vencedor` - Finaliza a partida e dá o prêmio.
    """
    await ctx.send(help_text)

if __name__ == '__main__':
    if TOKEN == 'SEU_TOKEN_AQUI':
        print("ERRO: Você precisa configurar seu Token do Discord no arquivo bot.py!")
    else:
        bot.run(TOKEN)
