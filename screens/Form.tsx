import { StyleSheet, Alert, View, TouchableOpacity, SafeAreaView } from 'react-native'
import { Camera, CameraType, FlashMode } from 'expo-camera'
import CameraPreview from '../components/CameraPreview'
import Button from '../components/Button'
import { useState, useRef } from 'react'

interface cameraStatus {
    status: string
}

export default function Form({ switchScreens }: { switchScreens: (status: string) => void }) {
    const [cameraStarted, setCameraStarted] = useState(false)
    const [previewVisible, setPreviewVisible] = useState(false)
    const [capturedImage, setCapturedImage] = useState<any>(null)
    const [type, setType] = useState(CameraType.back);
    const [flash, setFlash] = useState(FlashMode.off)
    const cameraRef: any = useRef(null);

    const takePicture = async () => {
        if (cameraRef) {
            try {
                const photo = await cameraRef.current.takePictureAsync();
                console.log(photo)
                setPreviewVisible(true)
                setCapturedImage(photo)
            } catch (e) {
                console.log(e)
            }
        }
    }

    const startCamera = async () => {
        //   MediaLibrary.requestPermissionsAsync();
        const cameraStatus: cameraStatus = await Camera.requestCameraPermissionsAsync();
        if (cameraStatus.status === "granted") setCameraStarted(true)
        else Alert.alert("Access denied")
    }

    const closeCamera = () => {
        setCameraStarted(false)
    }

    return (
        <SafeAreaView className='bg-black flex-1'>
            {cameraStarted ?
                previewVisible && capturedImage ? (
                    <CameraPreview photo={capturedImage} />
                ) : (
                    <Camera style={styles.camera} type={type} flashMode={flash} ref={cameraRef}>
                        <View
                            style={{
                                position: 'absolute',
                                top: 0,
                                flexDirection: 'row-reverse',
                                flex: 1,
                                width: '100%',
                                padding: 20,
                                marginTop: 30,
                                justifyContent: 'space-between'
                            }}><Button icon='cross' onPress={closeCamera} color="#fff" />
                        </View>
                        <View
                            style={{
                                position: 'absolute',
                                bottom: 0,
                                flexDirection: 'row',
                                flex: 1,
                                width: '100%',
                                padding: 20,
                                justifyContent: 'space-between'
                            }}>
                            <View
                                style={{
                                    alignSelf: 'center',
                                    flex: 1,
                                    alignItems: 'center'
                                }}>
                                <TouchableOpacity
                                    onPress={takePicture}
                                    style={{
                                        width: 70,
                                        height: 70,
                                        bottom: 0,
                                        borderRadius: 50,
                                        backgroundColor: '#fff'
                                    }} />
                            </View>
                        </View>
                    </Camera>
                )
                : (
                    <View className='flex-1'>
                        <View className='p-absolute flex-row '>
                            <Button title='Go to Dashboard' icon='back' onPress={() => switchScreens('Dashboard')} color="#fff" />
                        </View>
                        <View className='flex-1 justify-center'>
                            <Button title='Scan Document' icon='camera' onPress={startCamera} color="#fff" />
                        </View>
                    </View>
                )
            }
        </SafeAreaView>
    )
}

const styles = StyleSheet.create({

    camera: {
        flex: 1,
        width: '100%',
    }
})