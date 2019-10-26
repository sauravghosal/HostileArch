import React, { Component } from "react";
import { StyleSheet, Text, View, Button, Alert } from "react-native";
import Picture from "./components/Picture";
import Email from "./components/Email";
import Location from "./components/Location";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      location: false
    };
  }

  handleClick = event => {
    this.setState({
      location: true
    });
    console.log("clicked!");
  };

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>Hello</Text>
        <Button
          title="Get Location"
          onPress={e => this.handleClick(e)}
        ></Button>
        {this.state.location === true && <Location />}
      </View>
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
  instructions: {
    textAlign: "center",
    color: "#33333",
    marginBottom: 5
  }
});
