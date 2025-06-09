// App.tsx
import React, { useReducer, useCallback, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Button,
  TouchableOpacity,
  // @ts-ignore
  Picker,
  ImageBackground,
  Image,
} from 'react-native';
import { reducer, initialState, TYPES } from './AppReducer';
import { useMsgAfterSubmit } from './hooks';

import HeroSvg from './components/HeroSvg';
import bgSound from './assets/music/background-music.mp3';
import BackgroundSound from './components/BackgroundSound';

// Import the LSBU SVG as a component
import LsbuImage from './assets/images/lsbu.svg';

function App() {
  const [
    {
      answer,
      numOfEnemies,
      val1,
      val2,
      won,
      operator,
      mode,
      difficulty,
      modeType,
      previousNumOfEnemies,
      isStoredState,
      questionsAnswered,
      autoDifficultyEnabled,
      waveNumber,
      lastResult,
    },
    dispatch,
  ] = useReducer(reducer, initialState);

  const submitInputRef = React.useRef<TextInput>(null);

  const { msg, isErrorMessage } = useMsgAfterSubmit(lastResult);

  const handleAnswerChange = useCallback(
    (value: string) => {
      if (/^\d+|[.]$/.test(value.toString()) || value === '') {
        dispatch({ type: TYPES.SET_ANSWER, payload: value });
      }
    },
    [dispatch]
  );

  const handleModePicker = useCallback(
    (mode: string) => {
      dispatch({ type: TYPES.SET_MODE, payload: mode });
    },
    [dispatch]
  );

  const handleModeType = useCallback(
    (mode: string) => {
      dispatch({ type: TYPES.SET_MODE_TYPES, payload: mode });
    },
    [dispatch]
  );

  const handleDifficultyPicker = useCallback(
    (difficulty: string) => {
      dispatch({ type: TYPES.SET_DIFFICULTY, payload: difficulty });
    },
    [dispatch]
  );

  const handleRestart = useCallback(() => {
    dispatch({ type: TYPES.RESTART });
  }, [dispatch]);

  const handleFinish = useCallback(() => {
    dispatch({ type: TYPES.FINISH_GAME });
  }, [dispatch]);

  const handleSubmit = useCallback(() => {
    dispatch({ type: TYPES.CHECK_ANSWER });
    if (submitInputRef.current) submitInputRef.current.focus();
  }, [dispatch]);

  const activeTheme = themes[mode];

  useEffect(() => {
    dispatch({ type: TYPES.NEW_PROBLEM });
    const storedData = localStorage.getItem('state');
    if (storedData) {
      dispatch({ type: TYPES.RESTORE_STATE, payload: JSON.parse(storedData) });
    } else {
      localStorage.setItem('state', JSON.stringify({ ...initialState }));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(
      'state',
      JSON.stringify({
        answer,
        numOfEnemies,
        val1,
        val2,
        won,
        operator,
        mode,
        difficulty,
        modeType,
        previousNumOfEnemies,
        isStoredState,
        questionsAnswered,
        autoDifficultyEnabled,
        waveNumber,
        lastResult,
      })
    );
  }, [
    answer,
    numOfEnemies,
    won,
    val1,
    val2,
    operator,
    mode,
    difficulty,
    modeType,
    previousNumOfEnemies,
    isStoredState,
    questionsAnswered,
    autoDifficultyEnabled,
    waveNumber,
    lastResult,
  ]);

  const submitMsgText = isErrorMessage ? styles.msgTextError : styles.msgTextSuccess;
  const submitMessageBlock = !!msg && (
    <View style={styles.submitMsgWrapper}>
      <Text style={submitMsgText}>{msg}</Text>
    </View>
  );

  useEffect(() => {
    submitInputRef.current && submitInputRef.current.focus();
  });

  return (
    <View style={[styles.root, { backgroundColor: activeTheme.backgroundColor }]}>
      <ImageBackground
        source={require('./assets/images/bg.jpg')}
        style={styles.image}
        resizeMode="cover"
      >
        <Text style={[styles.title, { color: activeTheme.textColor }]}>
          Battle Math
        </Text>
        {/* Render the LSBU SVG as a component */}
        {/* <View>
          <LsbuImage width={200} height={200} />
        </View> */}

        <View style={styles.pickerContainer}>
          <Picker
            style={styles.picker}
            selectedValue={mode}
            onValueChange={handleModePicker}
            nativeID="operation-selector"
          >
            <Picker.Item label="Addition(+)" value="addition" />
            <Picker.Item label="Subtraction(-)" value="subtraction" />
            <Picker.Item label="Multiplication(*)" value="multiplication" />
            <Picker.Item label="Division(/)" value="division" />
          </Picker>

          <Picker
            selectedValue={difficulty}
            style={styles.picker}
            onValueChange={handleDifficultyPicker}
            nativeID="difficulty-selector"
          >
            <Picker.Item label="Easy" value="easy" />
            <Picker.Item label="Medium" value="medium" />
            <Picker.Item label="Hard" value="hard" />
          </Picker>

          <Picker
            selectedValue={modeType}
            style={styles.picker}
            onValueChange={handleModeType}
            nativeID="modeType-selector"
          >
            <Picker.Item label="Whole Number" value="wholeNumber" />
            <Picker.Item label="Decimals" value="decimal" />
          </Picker>

          <TouchableOpacity
            style={{
              marginLeft: 10,
              padding: 10,
              backgroundColor: 'gray',
              borderRadius: 6,
              alignSelf: 'center',
            }}
            onPress={() => dispatch({ type: TYPES.TOGGLE_AUTO_DIFFICULTY })}
          >
            <Text style={{ color: 'white' }}>
              {autoDifficultyEnabled ? 'Disable Auto' : 'Enable Auto'}
            </Text>
          </TouchableOpacity>
        </View>

        <Text style={{ color: '#fff', marginTop: 10 }}>
          Questions Answered: {questionsAnswered}
        </Text>
        <Text style={{ color: '#fff', marginTop: 5 }}>Wave: {waveNumber}</Text>

        <View style={styles.battlefield}>
          <View style={styles.container}>
            <View nativeID="hero">
              <Image
                source={require('./assets/images/hero.png')}
                style={{ width: 100, height: 200 }}
              />
            </View>
          </View>
          <View style={styles.container}>
            {[...Array(numOfEnemies)].map((_, i) => (
              <View testID="enemies" key={i}>
                <Image
                  source={require('./assets/images/orc.png')}
                  style={{ width: 100, height: 200 }}
                />
              </View>
            ))}
          </View>
        </View>

        {won ? (
          <View>
            <Text style={{ color: activeTheme.textColor }}>Victory!</Text>
            <Button
              onPress={handleRestart}
              title="Restart"
              color={activeTheme.buttonColor}
              accessibilityLabel="Click this button to play again."
            />
          </View>
        ) : (
          <View style={styles.mathContainer}>
            {submitMessageBlock}
            <View style={styles.mathRow}>
              <Text nativeID="val1" style={[styles.mathText, { color: activeTheme.textColor }]}>
                {val1}
              </Text>
              <Text nativeID="operator" style={[styles.mathText, { color: activeTheme.textColor }]}>
                {operator}
              </Text>
              <Text nativeID="val2" style={[styles.mathText, { color: activeTheme.textColor }]}>
                {val2}
              </Text>
              <Text style={[styles.mathText, { color: activeTheme.textColor }]}> = </Text>
              <TextInput
                nativeID="answer-input"
                style={styles.input}
                onChangeText={handleAnswerChange}
                onSubmitEditing={handleSubmit}
                value={answer}
                ref={submitInputRef}
              />
            </View>
            <TouchableOpacity
              style={[styles.button, { backgroundColor: activeTheme.buttonColor }]}
              testID="submit"
              onPress={handleSubmit}
              accessibilityLabel="Submit your answer"
            >
              <Text style={styles.buttonText}>Submit</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.button, { backgroundColor: activeTheme.buttonColor, marginTop: 10 }]}
              onPress={handleFinish}
            >
              <Text style={styles.buttonText}>Finish</Text>
            </TouchableOpacity>
          </View>
        )}
        <BackgroundSound url={bgSound} />
      </ImageBackground>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    alignItems: 'center',
    position: 'absolute',
    top: 0,
    bottom: 0,
    left: 0,
    right: 0,
  },
  image: {
    width: '100%',
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 16,
  },
  title: {
    fontSize: 32,
    fontFamily: `"Comic Sans MS", cursive, sans-serif`,
  },
  pickerContainer: {
    flexDirection: 'row',
  },
  picker: {
    height: 40,
    width: 150,
    borderRadius: 8,
    fontFamily: `"Comic Sans MS", cursive, sans-serif`,
    textAlign: 'center',
    marginLeft: 10,
  },
  battlefield: {
    flex: 1,
    flexDirection: 'row',
    width: '100%',
    paddingHorizontal: 16,
  },
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'space-evenly',
  },
  mathContainer: {
    paddingVertical: 16,
  },
  mathRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    paddingBottom: 16,
  },
  mathText: {
    fontSize: 40,
    fontFamily: `"Comic Sans MS", cursive, sans-serif`,
  },
  input: {
    height: 60,
    width: 200,
    borderColor: 'gray',
    borderWidth: 1,
    marginLeft: 8,
    color: '#fff',
    fontSize: 40,
    borderRadius: 8,
    fontFamily: `"Comic Sans MS", cursive, sans-serif`,
  },
  button: {
    height: 60,
    width: 200,
    backgroundColor: '#841584',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 40,
  },
  msgTextError: {
    color: 'red',
    fontSize: 25,
  },
  msgTextSuccess: {
    color: 'green',
    fontSize: 25,
  },
  submitMsgWrapper: {
    paddingBottom: 15,
    fontSize: 40,
    fontFamily: `"Comic Sans MS", cursive, sans-serif`,
  },
});

const themes = {
  addition: {
    backgroundColor: 'darkslateblue',
    heroColor: 'rgba(23, 190, 187, 1)',
    enemyColor: 'rgba(228, 87, 46, 1)',
    buttonColor: 'rgba(255, 201, 20, 1)',
    textColor: '#fff',
  },
  subtraction: {
    backgroundColor: 'deepskyblue',
    heroColor: 'rgba(23, 190, 187, 1)',
    enemyColor: 'rgba(228, 87, 46, 1)',
    buttonColor: 'rgba(255, 201, 20, 1)',
    textColor: '#000',
  },
  multiplication: {
    backgroundColor: 'darkslategrey',
    heroColor: 'rgba(23, 190, 187, 1)',
    enemyColor: 'rgba(228, 87, 46, 1)',
    buttonColor: 'rgba(255, 201, 20, 1)',
    textColor: '#fff',
  },
  division: {
    backgroundColor: 'turquoise',
    heroColor: 'rgba(23, 190, 187, 1)',
    enemyColor: 'rgba(228, 87, 46, 1)',
    buttonColor: 'rgba(255, 201, 20, 1)',
    textColor: '#000',
  },
};

export default App;
