import * as React from "react";
import { Button, Image, View, StyleSheet } from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as Permissions from "expo-permissions";
import { Ionicons } from "@expo/vector-icons";

export default class Camera extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image: null
    };
  }

  selectPicture = async () => {
    await Permissions.askAsync(Permissions.CAMERA_ROLL);
    const options = {
      mediaTypes: ImagePicker.MediaTypeOptions.Image,
      allowsEditing: true,
      aspect: [4, 3],
      base64: true
    };
    let result = await ImagePicker.launchImageLibraryAsync(options);

    this.props.changeBase64(result.base64);

    if (!result.cancelled) {
      this.setState({ image: result.uri });
    }
  };

  takePicture = async () => {
    await Permissions.askAsync(Permissions.CAMERA);
    const options = {
      mediaTypes: ImagePicker.MediaTypeOptions.Image,
      allowsEditing: true,
      aspect: [4, 3],
      base64: true
    };
    let result = await ImagePicker.launchCameraAsync(options);
    this.props.changeBase64(result.base64);

    if (!result.cancelled) {
      this.setState({ image: result.uri });
    }
  };

  render() {
    return (
      <View style={styles.container}>
        {this.state.image !== null && (
          <Image
            style={{ width: 400, height: 400 }}
            source={{ uri: this.state.image }}
          />
        )}
        <View style={styles.row}>
          {/* <Button title="Camera" onPress={this.takePicture}>
            Camera
          </Button> */}
          <Button title="Take or Select Photo" onPress={this.selectPicture}>
            Gallery
          </Button>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  button: {
    radius: 0.1
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5FCFF"
  },
  image: {
    flex: 1,
    width: null,
    height: null,
    resizeMode: "contain"
  },
  row: {
    flexDirection: "row"
  }
});
