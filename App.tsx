import { SafeAreaView, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera, CameraType, FlashMode } from 'expo-camera';
import * as MediaLibrary from "expo-media-library";
import { useEffect, useRef, useState } from 'react';
import Button from './components/Button';
import CameraPreview from './components/CameraPreview';
import Form from './screens/Form';
import Dashboard from './screens/Dashboard';



export default function App() {
  const [display, setDisplay] = useState('Dashboard')
  const switchScreens = (status: string) => {
    if (status === 'Pending') setDisplay('PendingForm')
    else if(status === 'Submitted') setDisplay('SubmittedForm')
    else setDisplay('Dashboard')
  }
  return (
    display === 'Dashboard' ?
      <Dashboard switchScreens={switchScreens} />
      : display === 'PendingForm' ?
        <Form switchScreens={switchScreens} />
        :
        <></>
  );
}
