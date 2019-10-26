import React from "react";
import { Text, View } from "react-native";
import FontAwesome, {
  SolidIcons,
  RegularIcons,
  BrandIcons,
  parseIconName
} from "react-native-fontawesome";

function Picture(props) {
  return (
    <View>
      <FontAwesome icon={parseIconFromClassName("fas fa-chevron-left")} />
    </View>
  );
}

export default Picture;
