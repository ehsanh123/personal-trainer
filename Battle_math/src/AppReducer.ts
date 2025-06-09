import { Reducer } from 'react'

export function randomNumberGenerator(
  min: number,
  max: number,
  modeType: string
): number {
  if (modeType.includes('decimal'))
    return Number.parseFloat((Math.random() * (max - min)).toFixed(2))
  else return Math.floor(Math.random() * (max - min)) + min
}

export const TYPES = {
  SET_ANSWER: 0,
  ADD_ENEMY: 1,
  REMOVE_ENEMY: 2,
  CHECK_ANSWER: 3,
  NEW_PROBLEM: 4,
  SET_MODE: 5,
  SET_DIFFICULTY: 6,
  RESTART: 7,
  SET_MODE_TYPES: 8,
  RESTORE_STATE: 9,
  INCREMENT_QUESTION_COUNT: 10,
  TOGGLE_AUTO_DIFFICULTY: 11,
  FINISH_GAME: 12,
} as const

const OPERATORS = {
  addition: '+',
  subtraction: '-',
  multiplication: '*',
  division: '/',
} as const

const DIFFICULTIES = {
  easy: 'easy',
  medium: 'medium',
  hard: 'hard',
} as const

const MODE_TYPES = {
  wholeNumber: 'wholeNumber',
  decimals: 'decimal',
} as const

export type ActionType = {
  type: typeof TYPES[keyof typeof TYPES]
  payload?: unknown
}

export type AppState = {
  answer: string
  numOfEnemies: number
  previousNumOfEnemies: number
  val1: number
  val2: number
  won: boolean
  operator: typeof OPERATORS[keyof typeof OPERATORS]
  mode: keyof typeof OPERATORS
  difficulty: keyof typeof DIFFICULTIES
  modeType: keyof typeof MODE_TYPES
  isStoredState: boolean
  questionsAnswered: number
  autoDifficultyEnabled: boolean
  waveNumber: number
  lastResult: string
}

export const initialState: AppState = {
  answer: '',
  numOfEnemies: 3,
  previousNumOfEnemies: 3,
  val1: 0,
  val2: 0,
  won: false,
  operator: '+',
  mode: 'addition',
  difficulty: 'easy',
  modeType: 'wholeNumber',
  isStoredState: true,
  questionsAnswered: 0,
  autoDifficultyEnabled: true,
  waveNumber: 1,
  lastResult: "none",
}

const THRESHOLD_MEDIUM = 5
const THRESHOLD_HARD = 10
const BASE_ENEMIES = 3

export const reducer: Reducer<AppState, ActionType> = (state, action) => {
  const randomNumber = (
    diff = state.difficulty,
    mode = state.mode,
    modeType = state.modeType
  ) => {
    let val1, val2
    let x = 1, y = 9

    switch (diff) {
      case 'medium': {
        x = 10
        y = 99
        break
      }
      case 'hard': {
        x = 100
        y = 999
        break
      }
    }

    val1 = randomNumberGenerator(x, y, modeType)

    switch (mode) {
      case 'division': {
        y = modeType.includes('decimal') ? y : Math.floor(y / val1)
        break
      }
      case 'subtraction': {
        y = val1
        break
      }
    }
    val2 = randomNumberGenerator(x, y, modeType)

    while (val1 % val2 !== 0 && mode === 'division' && modeType.includes('wholeNumber'))
      val2--

    return [val1, val2]
  }

  switch (action.type) {
    case TYPES.RESTART: {
      let val = randomNumber()
      switch (state.mode) {
        case 'division':
          state.operator = '/'
          break
        case 'subtraction':
          state.operator = '-'
          break
        case 'addition':
          state.operator = '+'
          break
        case 'multiplication':
          state.operator = '*'
          break
      }

      return {
        ...initialState,
        mode: state.mode,
        difficulty: state.difficulty,
        modeType: state.modeType,
        val1: val[0],
        val2: val[1],
        operator: state.operator,
      }
    }

    case TYPES.SET_ANSWER: {
      return {
        ...state,
        isStoredState: false,
        answer: action.payload as string,
      }
    }

    case TYPES.ADD_ENEMY: {
      return {
        ...state,
        previousNumOfEnemies: state.numOfEnemies,
        numOfEnemies: BASE_ENEMIES + (state.waveNumber - 1),
      }
    }

    case TYPES.REMOVE_ENEMY: {
      let newState = { ...state, previousNumOfEnemies: state.numOfEnemies }
      newState.numOfEnemies--

      if (newState.numOfEnemies === 0) {
        if (state.autoDifficultyEnabled) {
          const newWave = state.waveNumber + 1
          newState.waveNumber = newWave
          newState.numOfEnemies = BASE_ENEMIES + (newWave - 1)
          newState.previousNumOfEnemies = newState.numOfEnemies
          newState.lastResult = "waveClear"
        } else {
          newState.won = true
          newState.lastResult = "correct"
        }
      }
      return newState
    }

    case TYPES.CHECK_ANSWER: {
      let answer
      if (state.modeType) {
        if (state.modeType.includes('decimal'))
          answer = parseFloat(state.answer || '')
        else answer = parseInt(state.answer || '', 10)
      }

      let expected = eval(`${state.val1} ${state.operator} ${state.val2}`)
      expected = Number.parseFloat(expected.toFixed(2))
      console.log(expected)

      let nextState
      if (answer === expected) {
        nextState = reducer(state, { type: TYPES.REMOVE_ENEMY })
        nextState = { 
          ...nextState, 
          lastResult: nextState.numOfEnemies === (BASE_ENEMIES + (nextState.waveNumber - 1))
            ? "waveClear" 
            : "correct" 
        }
      } else {
        nextState = reducer(state, { type: TYPES.ADD_ENEMY })
        nextState = { ...nextState, lastResult: "wrong" }
      }

      const newState = reducer(nextState, { type: TYPES.NEW_PROBLEM })
      return reducer(newState, { type: TYPES.INCREMENT_QUESTION_COUNT })
    }

    case TYPES.NEW_PROBLEM: {
      let val = randomNumber()
      if (val[0] === state.val1 && val[1] === state.val2) {
        return reducer(state, { type: TYPES.NEW_PROBLEM })
      }
      return {
        ...state,
        val1: val[0],
        val2: val[1],
        answer: '',
        lastResult: "none",
      }
    }

    case TYPES.SET_MODE: {
      const mode = action.payload as keyof typeof OPERATORS
      let val = randomNumber(state.difficulty, mode, state.modeType)
      return {
        ...state,
        mode,
        val1: val[0],
        val2: val[1],
        operator: OPERATORS[mode],
      }
    }

    case TYPES.SET_DIFFICULTY: {
      const difficulty = action.payload as keyof typeof DIFFICULTIES
      let val = randomNumber(difficulty, state.mode, state.modeType)
      return {
        ...state,
        difficulty,
        val1: val[0],
        val2: val[1],
      }
    }

    case TYPES.SET_MODE_TYPES: {
      const modeType = action.payload as keyof typeof MODE_TYPES
      let val = randomNumber(state.difficulty, state.mode, modeType)
      return {
        ...state,
        modeType,
        val1: val[0],
        val2: val[1],
      }
    }

    case TYPES.RESTORE_STATE: {
      const storedState = action.payload as AppState
      return { ...storedState, isStoredState: true }
    }

    case TYPES.INCREMENT_QUESTION_COUNT: {
      let updatedState = {
        ...state,
        questionsAnswered: state.questionsAnswered + 1,
      }
      if (updatedState.autoDifficultyEnabled) {
        if (
          updatedState.questionsAnswered >= THRESHOLD_HARD &&
          updatedState.difficulty !== 'hard'
        ) {
          updatedState.difficulty = 'hard'
        } else if (
          updatedState.questionsAnswered >= THRESHOLD_MEDIUM &&
          updatedState.difficulty === 'easy'
        ) {
          updatedState.difficulty = 'medium'
        }
      }
      return updatedState
    }

    case TYPES.TOGGLE_AUTO_DIFFICULTY: {
      return {
        ...state,
        autoDifficultyEnabled: !state.autoDifficultyEnabled,
      }
    }

    case TYPES.FINISH_GAME: {
      return {
        ...state,
        won: true,
      }
    }

    default:
      throw new Error(`Invalid action ${action.type}`)
  }

  return state
}
