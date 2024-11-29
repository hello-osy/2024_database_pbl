<template>
    <div class="background">
        <div class="contactBox" @click.self="closeContactBox">
            <slot> Default Information </slot>
            <p>Type here the problem</p>
            <input type="text">
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        closeContactBox() {
            this.$emit('closeContactBox')
        }
    }
}
</script>

<style scoped>
.background {
    top: 0;
    position: fixed; 
    background: rgba(0, 0, 0, 0.5);
    width: 100%;
    height: 100%;
}
.contactBox {
    width: 400px;
    padding: 20px;
    margin: 200px 160px;
    background: white;
    border-radius: 10px;
}
.contactBox h1 {
    color: #03cbf4;
    border: none;
    padding: 0;
}
.contactBox input[type="text"] {
    width: 100%; /* Makes the input stretch to the width of the .contactBox */
    padding: 10px; /* Adds some padding inside the input for better text visibility */
    margin-top: 10px; /* Adds some space above the input */
    border: 1px solid #ccc; /* Adds a subtle border to the input */
    border-radius: 5px; /* Rounds the corners of the input field */
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); /* Subtle shadow inside the input */
    transition: border-color 0.3s; /* Smooth transition for focus highlight */
}

.contactBox input[type="text"]:focus {
    border-color: #03cbf4; /* Changes border color to light blue when focused */
    outline: none; /* Removes the default focus outline */
}

</style>