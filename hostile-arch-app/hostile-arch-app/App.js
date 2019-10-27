import React, { Component } from "react";
import {
  StyleSheet,
  View,
  Button,
  TextInput,
  Animated,
  KeyboardAvoidingView,
  ActivityIndicator,
  TouchableHighlight,
  Text,
  Image,
  TouchableOpacity
} from "react-native";
import Location from "./components/Location";
import Camera from "./components/Camera";
import BootstrapStyleSheet from 'react-native-bootstrap-styles';


export default class App extends Component {
  constructor(props) {
    super(props);
    this.paddingInput = new Animated.Value(0);
    this.state = {
      location: false,
      imgBase64: null,
      lng: null,
      lat: null,
      date: new Date()
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
      lng: newLong
    });
  };

  submit = () => {
    const body = {
      x: this.state.lng,
      y: this.state.lat,
      text: this.state.description,
      picture_base_64: this.state.imgBase64,
      sender_email: this.state.senderEmail,
      name: this.state.name,
      timestamp: this.state.date
    };
    console.log(body);
    fetch("https://test-hack-gt-6.appspot.com/posting_email_info", {
      method: "POST",
      headers: {
        Accept: "application/json, text/plain, */*", // It can be used to overcome cors errors
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    })
      .then(response => response.text())
      .then(responseJson => {
        console.log(responseJson);
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
        <Button
          title="Get Location"
          onPress={event => this.setState({ location: true })}
        ></Button>
        {this.state.location === true && (
          <Location
            changeLat={this.changeLat.bind(this)}
            changeLong={this.changeLong.bind(this)}
          />
        )}
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
          <TextInput
            placeholder="Enter your name"
            style={styles.email}
            onChangeText={text => this.setState({ name: text })}
          />
        </View>
        {/* <Button title="Submit" onPress={this.submit}></Button> */}
        <TouchableOpacity title="Submit" onPress={this.submit} style={{ backgroundImage: "../assets/blue.png", borderWidth: 1, height: 42, width: "70%",
            justifyContent: "center", alignItems: "center", alignSelf: "center", borderRadius: 20, marginBottom: 50,
          }}>
          <Text> Submit </Text>
          </TouchableOpacity>
      </KeyboardAvoidingView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5FCFF",
    // backgroundImage: "../assets/blue.png"
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
    marginLeft: 10,
  }
});
