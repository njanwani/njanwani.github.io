---
permalink: /wordle
title: "Wordle"
author_profile: false
layout: single
---

<style>
  .wordle-container {
    margin: 0 auto;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    padding: 20px;
    max-width: var(--container-width, 500px);
  }
  
  .game-board {
    display: grid;
    grid-template-rows: repeat(6, 1fr);
    gap: 5px;
    margin-bottom: 20px;
  }
  
  .row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
  }
  
  .tile {
    width: var(--tile-size, 62px);
    height: var(--tile-size, 62px);
    border: 2px solid #d3d6da;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: var(--font-size, 32px);
    font-weight: bold;
    text-transform: uppercase;
    color: #000;
  }
  
  .tile.filled {
    border-color: #878a8c;
  }
  
  .tile.correct {
    background-color: #6aaa64;
    border-color: #6aaa64;
    color: white;
  }
  
  .tile.present {
    background-color: #c9b458;
    border-color: #c9b458;
    color: white;
  }
  
  .tile.absent {
    background-color: #787c7e;
    border-color: #787c7e;
    color: white;
  }
  
  .keyboard {
    margin-top: 30px;
  }
  
  .keyboard-row {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin-bottom: 8px;
  }
  
  .key {
    padding: 12px 8px;
    min-width: 40px;
    background-color: #d3d6da;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    text-transform: uppercase;
  }
  
  .key:hover {
    opacity: 0.8;
  }
  
  .key.wide {
    min-width: 65px;
  }
  
  .key.correct {
    background-color: #6aaa64;
    color: white;
  }
  
  .key.present {
    background-color: #c9b458;
    color: white;
  }
  
  .key.absent {
    background-color: #787c7e;
    color: white;
  }
  
  .message {
    text-align: center;
    margin: 20px 0;
    font-size: 18px;
    font-weight: bold;
    min-height: 30px;
  }
  
  .reset-btn {
    display: block;
    margin: 20px auto;
    padding: 12px 24px;
    background-color: #6aaa64;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .reset-btn:hover {
    opacity: 0.9;
  }
</style>

<div class="wordle-container">
  <div class="message" id="message"></div>
  <div class="game-board" id="board"></div>
  <div class="keyboard" id="keyboard"></div>
  <button class="reset-btn" id="reset-btn" style="display: none;">Play Again</button>
</div>

<script>
  const WORDS = [
    'ELEPHANT', 'COMPUTER', 'MOUNTAIN', 'KEYBOARD', 'UNIVERSE',
    'CAT', 'DOG', 'BAT', 'SUN', 'SKY', 'BED',
    'SCIENCE', 'PICTURE', 'TEACHER'
  ];
  
  let targetWord = '';
  let currentRow = 0;
  let currentTile = 0;
  let gameOver = false;
  let keyboardState = {};
  let wordLength = 0;
  let maxGuesses = 0;
  
  const board = document.getElementById('board');
  const keyboard = document.getElementById('keyboard');
  const message = document.getElementById('message');
  const resetBtn = document.getElementById('reset-btn');
  
  const keyboardLayout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACKSPACE']
  ];
  
  function initGame() {
    targetWord = WORDS[Math.floor(Math.random() * WORDS.length)];
    wordLength = targetWord.length;
    maxGuesses = wordLength - 1;
    currentRow = 0;
    currentTile = 0;
    gameOver = false;
    keyboardState = {};
    message.textContent = '';
    resetBtn.style.display = 'none';
    
    // Calculate tile size and container width based on word length
    const gap = 5;
    let tileSize, containerWidth;
    
    if (wordLength <= 5) {
      tileSize = 62;
      containerWidth = 500;
    } else if (wordLength <= 7) {
      tileSize = 55;
      containerWidth = wordLength * tileSize + (wordLength - 1) * gap + 40;
    } else {
      tileSize = Math.max(40, Math.floor(650 / wordLength));
      containerWidth = wordLength * tileSize + (wordLength - 1) * gap + 40;
    }
    
    const fontSize = Math.max(20, Math.floor(tileSize * 0.52));
    
    // Set CSS variables
    document.documentElement.style.setProperty('--tile-size', `${tileSize}px`);
    document.documentElement.style.setProperty('--font-size', `${fontSize}px`);
    document.documentElement.style.setProperty('--container-width', `${containerWidth}px`);
    
    // Create board
    board.innerHTML = '';
    for (let i = 0; i < maxGuesses; i++) {
      const row = document.createElement('div');
      row.className = 'row';
      for (let j = 0; j < wordLength; j++) {
        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.id = `tile-${i}-${j}`;
        row.appendChild(tile);
      }
      board.appendChild(row);
    }
    
    // Create keyboard
    keyboard.innerHTML = '';
    keyboardLayout.forEach(row => {
      const keyRow = document.createElement('div');
      keyRow.className = 'keyboard-row';
      row.forEach(key => {
        const keyButton = document.createElement('button');
        keyButton.className = 'key';
        if (key === 'ENTER' || key === 'BACKSPACE') {
          keyButton.classList.add('wide');
          keyButton.textContent = key === 'BACKSPACE' ? '⌫' : key;
        } else {
          keyButton.textContent = key;
        }
        keyButton.dataset.key = key;
        keyButton.addEventListener('click', () => handleKeyPress(key));
        keyRow.appendChild(keyButton);
      });
      keyboard.appendChild(keyRow);
    });
  }
  
  function handleKeyPress(key) {
    if (gameOver) return;
    
    if (key === 'BACKSPACE') {
      if (currentTile > 0) {
        currentTile--;
        const tile = document.getElementById(`tile-${currentRow}-${currentTile}`);
        tile.textContent = '';
        tile.classList.remove('filled');
      }
    } else if (key === 'ENTER') {
      if (currentTile === wordLength) {
        checkGuess();
      }
    } else if (currentTile < wordLength) {
      const tile = document.getElementById(`tile-${currentRow}-${currentTile}`);
      tile.textContent = key;
      tile.classList.add('filled');
      currentTile++;
    }
  }
  
  function checkGuess() {
    const guess = [];
    for (let i = 0; i < wordLength; i++) {
      const tile = document.getElementById(`tile-${currentRow}-${i}`);
      guess.push(tile.textContent);
    }
    const guessWord = guess.join('');
    
    // Color the tiles
    const letterCount = {};
    for (let char of targetWord) {
      letterCount[char] = (letterCount[char] || 0) + 1;
    }
    
    const result = Array(wordLength).fill('absent');
    
    // First pass: mark correct positions
    for (let i = 0; i < wordLength; i++) {
      if (guess[i] === targetWord[i]) {
        result[i] = 'correct';
        letterCount[guess[i]]--;
      }
    }
    
    // Second pass: mark present letters
    for (let i = 0; i < wordLength; i++) {
      if (result[i] === 'absent' && letterCount[guess[i]] > 0) {
        result[i] = 'present';
        letterCount[guess[i]]--;
      }
    }
    
    // Apply colors to tiles
    for (let i = 0; i < wordLength; i++) {
      const tile = document.getElementById(`tile-${currentRow}-${i}`);
      tile.classList.add(result[i]);
      
      // Update keyboard state
      const letter = guess[i];
      if (result[i] === 'correct') {
        keyboardState[letter] = 'correct';
      } else if (result[i] === 'present' && keyboardState[letter] !== 'correct') {
        keyboardState[letter] = 'present';
      } else if (!keyboardState[letter]) {
        keyboardState[letter] = 'absent';
      }
    }
    
    // Update keyboard colors
    updateKeyboard();
    
    // Check win condition
    if (guessWord === targetWord) {
      message.textContent = '🎉 You won!';
      gameOver = true;
      resetBtn.style.display = 'block';
      return;
    }
    
    // Move to next row
    currentRow++;
    currentTile = 0;
    
    // Check lose condition
    if (currentRow === maxGuesses) {
      message.textContent = `Game over! The word was ${targetWord}`;
      gameOver = true;
      resetBtn.style.display = 'block';
    }
  }
  
  function updateKeyboard() {
    for (let letter in keyboardState) {
      const keyButton = document.querySelector(`[data-key="${letter}"]`);
      if (keyButton) {
        keyButton.classList.remove('correct', 'present', 'absent');
        keyButton.classList.add(keyboardState[letter]);
      }
    }
  }
  
  // Physical keyboard support
  document.addEventListener('keydown', (e) => {
    const key = e.key.toUpperCase();
    if (key === 'BACKSPACE') {
      handleKeyPress('BACKSPACE');
    } else if (key === 'ENTER') {
      handleKeyPress('ENTER');
    } else if (/^[A-Z]$/.test(key)) {
      handleKeyPress(key);
    }
  });
  
  resetBtn.addEventListener('click', initGame);
  
  // Initialize game on load
  initGame();
</script>
