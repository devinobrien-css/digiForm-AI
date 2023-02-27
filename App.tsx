import { SafeAreaView, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera, CameraType, FlashMode } from 'expo-camera';
import * as MediaLibrary from "expo-media-library";
import { useEffect, useRef, useState } from 'react';
import Button from './components/Button';
import CameraPreview from './components/CameraPreview';
import Form from './screens/Form';
import Dashboard from './screens/Dashboard';
import Fill_Form from './screens/Fill_Form';



export default function App() {
  const [display, setDisplay] = useState('Dashboard')
  const switchScreens = (screen: string) => {
    if (screen === 'Form') setDisplay('PendingForm')
    else if(screen === 'Fill Form') setDisplay('Fill Form')
    else setDisplay('Dashboard')
  }
  return (
    display === 'Dashboard' ?
      <Dashboard switchScreens={switchScreens} />
      : display === 'PendingForm' ?
        <Form switchScreens={switchScreens} />
        : display === 'Fill Form' ?
          <Fill_Form></Fill_Form>
        :
        <></>
  );
}
