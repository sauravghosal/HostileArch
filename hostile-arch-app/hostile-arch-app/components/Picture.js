import React from "react";
import { Text, View, StyleSheet } from "react-native";
import { Ionicons, FontAwesome } from "@expo/vector-icons";

const styles = StyleSheet.create({
  scene: {
    backgroundColor: "#F9E8D5",
    flex: 1,
    justifyContent: "flex-start",
    alignItems: "center",
    flexDirection: "column"
  },
  card: {
    backgroundColor: "#E6D5C3",
    flex: 0.2,
    flexDirection: "column",
    marginTop: "20%" // Replace by 20
  },
  container: {
    backgroundColor: "#FFFFFF",
    flex: 1,
    flexDirection: "column",
    justifyContent: "center"
  }
});

function Picture(props) {
  return (
    <View style={styles.scene}>
      {/* Figure out icons here */}
      <FontAwesome name="camera" size={50} onp />
    </View>
  );
}

export default Picture;
