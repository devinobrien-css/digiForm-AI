import { View, ImageBackground } from "react-native"

export default function CameraPreview ({photo}: any) {
    return (
      <View
        style={{
          backgroundColor: 'transparent',
          flex: 1,
          width: '100%',
          height: '100%'
        }}
      >
        <ImageBackground
          source={{uri: photo.uri}}
          style={{
            flex: 1
          }}
        />
      </View>
    )
  }