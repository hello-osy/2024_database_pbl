<template>
  <component
    :is="tag"
    @click.native="hideSidebar"
    class="nav-item"
    v-bind="$attrs"
    tag="li"
  >
    <a class="nav-link">
      <slot>
        <i v-if="icon" :class="icon"></i>
        <p>{{ name }}</p>
      </slot>
      <i v-if="hasSubMenu" :class="arrowIcon" class="arrow-icon" @click.stop="toggleSubMenu"></i>
    </a>
    <ul v-if="isSubMenuVisible" class="sub-menu">
      <li v-for="(child, index) in children" :key="index">
        <router-link :to="child.path" class="sub-menu-link">
          {{ child.name }}
        </router-link>
      </li>
    </ul>
  </component>
</template>
<script>
export default {
  name: "sidebar-link",
  inheritAttrs: false,
  inject: {
    autoClose: {
      default: true,
    },
    addLink: {
      default: () => {},
    },
    removeLink: {
      default: () => {},
    },
  },
  props: {
    name: String,
    icon: String,
    tag: {
      type: String,
      default: "router-link",
    },
    children: {
      type: Array,
      default: () => [],
    }
  },
  computed: {
    hasSubMenu() {
      // 서브메뉴가 있는지 확인
      return this.children && this.children.length > 0;
    },
    arrowIcon() {
      // 화살표 아이콘 변경
      return this.isSubMenuVisible
        ? "ti-angle-up"
        : "ti-angle-down";
    },
  },
  data() {
    return {
      isSubMenuVisible: false, // 서브 메뉴 표시 상태
    };
  },
  methods: {
    toggleSubMenu() {
        this.isSubMenuVisible = !this.isSubMenuVisible; // 서브 메뉴 표시 토글
    },
    hideSidebar() {
      if (this.autoClose) {
        this.$sidebar.displaySidebar(false);
      }
    },
    isActive() {
      return this.$el.classList.contains("active");
    },
  },
  mounted() {
    if (this.addLink) {
      this.addLink(this);
    }
  },
  beforeDestroy() {
    if (this.$el && this.$el.parentNode) {
      this.$el.parentNode.removeChild(this.$el);
    }
    if (this.removeLink) {
      this.removeLink(this);
    }
  },
};
</script>
<style>
</style>
