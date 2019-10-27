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
import BootstrapStyleSheet from "react-native-bootstrap-styles";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.paddingInput = new Animated.Value(0);
    this.state = {
      submit: "not yet",
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
        if (responseJson === "Thank you for being a good citizen.") {
          this.setState({
            submit: "success"
          });
        } else {
          this.setState({
            submit: "err"
          });
        }
      })
      .catch(error => {
        this.setState({
          submit: "err"
        });
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

        {this.state.location ? (
          <TouchableOpacity
            title="Location Button"
            onPress={this.submit}
            style={styles.buttonSuccessLocation}
          >
            <Text style={{ color: "white" }}> Received! </Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity
            title="Location Button"
            onPress={event => {
              this.setState({ location: true });
            }}
            style={styles.buttonInitialLocation}
          >
            <Text style={{ color: "white" }}> Get Location </Text>
          </TouchableOpacity>
        )}

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
            style={styles.name}
            onChangeText={text => this.setState({ name: text })}
          />
        </View>

        {this.state.submit === "not yet" && (
          <TouchableOpacity
            title="Submit"
            onPress={this.submit}
            style={styles.buttonInitialSubmit}
          >
            <Text style={{ color: "white" }}> Submit </Text>
          </TouchableOpacity>
        )}

        {this.state.submit === "success" && (
          <TouchableOpacity title="Submit" style={styles.buttonSuccessSubmit}>
            <Text style={{ color: "white" }}> Success! </Text>
          </TouchableOpacity>
        )}

        {this.state.submit == "err" && (
          <TouchableOpacity
            title="Submit"
            style={styles.buttonError}
            onPress={this.submit}
          >
            <Text style={{ color: "white" }}> Try Again </Text>
          </TouchableOpacity>
        )}
      </KeyboardAvoidingView>
    );
  }
}

const styles = StyleSheet.create({
  buttonInitialLocation: {
    backgroundColor: "royalblue",
    fontColor: "white",
    borderWidth: 0,
    height: 42,
    width: "70%",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    borderRadius: 20,
    marginBottom: 20
  },
  buttonInitialSubmit: {
    backgroundColor: "royalblue",
    fontColor: "white",
    borderWidth: 0,
    height: 42,
    width: "70%",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    borderRadius: 20,
    marginBottom: 55
  },
  buttonSuccessLocation: {
    backgroundColor: "lightgreen",
    fontColor: "white",
    borderWidth: 0,
    height: 42,
    width: "70%",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    borderRadius: 20,
    marginBottom: 20
  },
  buttonSuccessSubmit: {
    backgroundColor: "lightgreen",
    fontColor: "white",
    borderWidth: 0,
    height: 42,
    width: "70%",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    borderRadius: 20,
    marginBottom: 55
  },
  buttonError: {
    backgroundColor: "red",
    fontColor: "white",
    borderWidth: 0,
    height: 42,
    width: "70%",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    borderRadius: 20,
    marginBottom: 55
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5FCFF"
    // backgroundImage: "../assets/blue.png"
  },
  welcome: {
    fontSize: 20,
    textAlign: "center",
    margin: 10
  },
  textInput: {
    marginBottom: 50,
    backgroundColor: "#F5FCFF"
  },
  description: {
    height: 50,
    width: 480,
    borderColor: "gray",
    borderWidth: 1,
    borderBottomWidth: 0.45,
    textAlign: "center",
    marginLeft: 10
  },
  email: {
    height: 50,
    width: 480,
    borderColor: "gray",
    borderWidth: 1,
    borderTopWidth: 0.45,
    textAlign: "center",
    marginLeft: 10,
    borderBottomWidth: 0.45
  },
  name: {
    height: 50,
    width: 480,
    borderColor: "gray",
    borderWidth: 1,
    borderTopWidth: 0.45,
    textAlign: "center",
    marginLeft: 10,
    borderBottomWidth: 1
  }
});
