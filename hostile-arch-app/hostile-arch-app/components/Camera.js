import * as React from 'react';
import { Button, Image, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Constants from 'expo-constants';
import * as Permissions from 'expo-permissions';
import styles from './styles';

export default class Camera extends React.Component {
  state = {
    image: null,
  };

  selectPicture = async() => {
    await Permissions.askAsync(Permissions.CAMERA_ROLL);
    let result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.All,
        allowsEditing: true,
        aspect: [4, 3],
        base64: true,
      });
  
      console.log(result);
  
      if (!result.cancelled) {
        this.setState({ image: result.uri });
      }
  }

  takePicture = async() => {
    await Permissions.askAsync(Permissions.CAMERA);
    let result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.All,
        allowsEditing: true,
        aspect: [4, 3],
        base64: true,
      });
  
      console.log(result);
  
      if (!result.cancelled) {
        this.setState({ image: result.uri });
      }
  };

  render() {
      return (
          <View style={styles.container}>
              <Image style={styles.image} source ={{ uri: this.state.image }} />
                <View style={styles.row}>
                    <Button title="Gallery" onPress={this.selectPicture}>Gallery</Button>
                    <Button title="Camera" onPress={this.takePicture}>Camera</Button>
                </View>
          </View>
      )
  }
}