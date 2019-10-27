import React, { Component } from "react";
import {
  StyleSheet,
  Text,
  View,
  Button,
  Alert,
  TextInput,
  ScrollView,
  Animated,
  Keyboard,
  KeyboardAvoidingView,
  TextTranslateInput
} from "react-native";
import Location from "./components/Location";
import Camera from "./components/Camera";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.paddingInput = new Animated.Value(0);
    this.state = {
      imgBase64: null,
      x: null,
      y: null
    };
  }

  // Setters for imgBase64, changeLong, and changeLat

  changeBase64 = newBase64 => {
    this.setState({
      imgBase64: newBase64
    });
  };

  changeLat = newLat => {
    this.setState({
      lat: newLat
    });
  };

  changeLong = newLong => {
    this.setState({
      long: newLong
    });
  };

  submit = () => {
    console.log("hello!");
    fetch("https://test-hack-gt-6.appspot.com/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      mess: JSON.stringify({
        x: this.state.x,
        y: this.state.y,
        text: this.state.description,
        picture_base_64: this.state.imgBase64,
        sender_email: this.state.senderEmail
      })
    })
      .then(response => response.json())
      .then(responseJson => {
        return responseJson.movies;
      })
      .catch(error => {
        console.error(error);
      });
  };

  render() {
    return (
      <KeyboardAvoidingView
        keyboardDismissMode="on-drag"
        style={styles.container}
        behavior="padding"
        enabled
      >
        <Camera changeBase64={this.changeBase64.bind(this)} />
        <View style={styles.textInput}>
          <TextInput
            placeholder="Enter image description here!"
            style={styles.description}
            onChangeText={text => this.setState({ description: text })}
          />
          <TextInput
            placeholder="Enter email address! (Optional)"
            style={styles.email}
            onChangeText={text => this.setState({ senderEmail: text })}
          />
        </View>
        <Button title="Submit" onPress={this.submit}></Button>
      </KeyboardAvoidingView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5FCFF"
  },
  welcome: {
    fontSize: 20,
    textAlign: "center",
    margin: 10
  },
  image: {},
  textInput: {
    marginBottom: 50,
    backgroundColor: "#F5FCFF"
  },
  instructions: {
    textAlign: "center",
    marginBottom: 5
  },
  description: {
    height: 40,
    width: 480,
    borderColor: "gray",
    borderWidth: 1,
    borderBottomWidth: 0.45,
    textAlign: "center",
    marginLeft: 10
  },
  email: {
    height: 40,
    width: 480,
    borderColor: "gray",
    borderWidth: 1,
    borderTopWidth: 0.45,
    textAlign: "center",
    marginLeft: 10
  }
});
