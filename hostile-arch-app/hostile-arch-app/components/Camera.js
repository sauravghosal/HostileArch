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
      const { cancelled, uri } = await ImagePicker.launchImageLibraryAsync({
          aspect: 1,
          allowsEditing: true,
          base64: true,
      });
      this.setState({ image: uri});
      if (!cancelled) this.setState({ image: uri});
      console.log(this.state);
  }

  takePicture = async() => {
      await Permissions.askAsync(Permissions.CAMERA);
      const { cancelled, uri } = await ImagePicker.launchCameraAsync({
          allowsEditing: false,
          base64: true,
      });
      this.setState({ image : uri});
      console.log(this.state);
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

//   render() {
//     let { image } = this.state;

//     return (
//       <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
//         <Button
//           title="Pick an image from camera roll"
//           onPress={this._pickImage}
//         />
//         {image &&
//           <Image source={{ uri: image }} style={{ width: 200, height: 200 }} 
//           />}
//       </View>
//     );
//   }

//   componentDidMount() {
//     this.getPermissionAsync();
//   }

//   getPermissionAsync = async () => {
//     if (Constants.platform.ios) {
//       const { status } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
//       if (status !== 'granted') {
//         alert('Sorry, we need camera roll permissions to make this work!');
//       }
//     }
//   }

//   _takePicture = async() => {
//       let result = await ImagePicker.launchCameraAsync({
//           allowsEditing: false,
//       });
//       this.setState({ image : uri });
//   }

//   _pickImage = async () => {
//     let result = await ImagePicker.launchImageLibraryAsync({
//       mediaTypes: ImagePicker.MediaTypeOptions.All,
//       allowsEditing: true,
//       aspect: [4, 3],
//     });

//     console.log(result);

//     if (!result.cancelled) {
//       this.setState({ image: result.uri });
//     }
//   };
}