# Bot de Apostas Free Fire (Discord)

Este é um bot simples para gerenciar apostas de Free Fire em servidores do Discord usando uma moeda fictícia.

## 🚀 Funcionalidades
- **Cadastro**: Jogadores começam com 1000 moedas.
- **Apostas**: Admins criam partidas com taxa de entrada.
- **Vencedores**: Admins definem quem ganhou e o prêmio é distribuído automaticamente.
- **Ranking**: Veja quem são os jogadores com maior saldo.

## 🛠️ Como Configurar

1. **Obter um Token**:
   - Vá para o [Discord Developer Portal](https://discord.com/developers/applications).
   - Crie uma nova aplicação e um Bot.
   - Ative as **Privileged Gateway Intents** (`Presence Intent`, `Server Members Intent`, `Message Content Intent`).
   - Copie o **Token** do bot.

2. **Instalar Dependências**:
   ```bash
   pip install discord.py
   ```

3. **Configurar o Código**:
   - Abra o arquivo `bot.py`.
   - Substitua `'SEU_TOKEN_AQUI'` pelo token que você copiou.

4. **Rodar o Bot**:
   ```bash
   python bot.py
   ```

## 🎮 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `!cadastro` | Cria sua conta e ganha 1000 moedas. |
| `!saldo` | Verifica seu saldo atual. |
| `!apostar <id>` | Entra em uma partida aberta pagando a taxa. |
| `!ranking` | Mostra os 5 jogadores mais ricos. |
| `!ajuda_ff` | Lista todos os comandos. |

### Comandos de Administrador
- `!criar_partida <id> <taxa> <descrição>`: Cria uma nova aposta.
- `!vencedor <id> @usuário`: Finaliza a partida e entrega o prêmio ao vencedor.

---
*Nota: Este bot utiliza apenas moeda fictícia para entretenimento.*
