# 🎮 Intelligent Tic-Tac-Toe AI

A multi-agent adversarial Tic-Tac-Toe game implementing classic AI algorithms **Minimax** and **Alpha-Beta Pruning**, with integration of Google's **Gemini API** as an external decision-making agent.

Built for **CP468: Artificial Intelligence**, this project supports both CLI and GUI gameplay with visualization and benchmarking tools.


---

## 🧠 Agents Implemented

| Agent         | Description                                                   |
|---------------|---------------------------------------------------------------|
| **Minimax**   | Exhaustive search through the entire decision tree            |
| **Alpha-Beta**| Optimized version of Minimax with branch pruning              |
| **Gemini**    | Uses Google Gemini LLM to predict moves via API               |
| **Human**     | Manual input via keyboard (console or GUI)                    |

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
### 2. Start The Game
```bash
python src/main.py
```
You’ll be prompted to:
- Select Game Mode (Human vs AI / AI vs AI / Benchmark)

- Choose Visualization (Console or GUI)

- Choose Board Size (3x3 or 5x5)

- Select AI depth (default: 4–9)

## 🔑 Gemini API Setup
1. Go to **config/gemini_config.json**
2. Add your Gemini API key like this:

```bash
{
  "GEMINI_API_KEY": "your-api-key-here"
}
```
- You can also use a **.env** file with **GEMINI_API_KEY=your-key**
If the key is missing or quota is exceeded, the Gemini agent will automatically fall back to random moves.

## 📊 Benchmark Mode
- Runs 5 games per AI matchup
- Tracks:
  - Nodes Evaluated

  - Execution Time

  - Win/Draw Stats

To run:
```bash
python src/main.py
# Select Mode 6: Benchmark
```
## 🌳 Tree Visualizations
- Automatically saved under **results/visualizations/**

- Shows how each AI explores the game tree

- Red = Pruned (Alpha-Beta), Green = Win, Blue = Loss, Yellow = Draw

## 📈 Example Output
- Benchmark charts

- Console logs with execution times

- Visual game trees (Minimax vs Alpha-Beta)

## 📚 References

- Artificial Intelligence: A Modern Approach – Russell & Norvig

- Google Gemini API Docs

- Python: **pygame**, **networkx**, **matplotlib**, **google-generativeai**

## 💡 Future Ideas
- Extend to 5x5 board with heuristics

- Add reinforcement learning agents

- Build smarter Gemini prompts or retry handling

- Upgrade GUI with animations and score tracking
