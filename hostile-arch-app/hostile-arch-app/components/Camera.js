import * as React from "react";
import { Button, Image, View } from "react-native";
import * as ImagePicker from "expo-image-picker";
import Constants from "expo-constants";
import * as Permissions from "expo-permissions";
import styles from "./styles";

export default class Camera extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image: null
    };
  }

  selectPicture = async () => {
    await Permissions.askAsync(Permissions.CAMERA_ROLL);
    const { cancelled, uri } = await ImagePicker.launchImageLibraryAsync({
      aspect: 1,
      allowsEditing: true,
      base64: true
    });
    this.setState({ image: uri });
    if (!cancelled) this.setState({ image: uri });
  };

  takePicture = async () => {
    await Permissions.askAsync(Permissions.CAMERA);
    const { cancelled, uri } = await ImagePicker.launchCameraAsync({
      base64: true,
      // change
      quality: 0.75
    });
    console.log(uri);
  };

  render() {
    return (
      <View style={styles.container}>
        <Image style={styles.image} source={{ uri: this.state.image }} />
        <View style={styles.row}>
          <Button title="Gallery" onPress={this.selectPicture}>
            Gallery
          </Button>
          <Button title="Camera" onPress={this.takePicture}>
            Camera
          </Button>
        </View>
      </View>
    );
  }
}
