<template>
  <div>
    <token />
  </div>
</template>

<script>
import Token from "@/components/Token";

export default {
  name: "home",
  components: {
    Token
  }
};
</script>

<style lang="scss" scoped>
.next-steps {
  .fa-link {
    margin-right: 5px;
  }
}
</style>
