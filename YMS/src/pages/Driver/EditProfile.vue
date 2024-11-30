<template>
    <div class="edit-profile-container">
      <h1>Edit Profile</h1>
      <form @submit.prevent="handleSubmit"> 
        <label> Email: </label>
        <input type="email" required v-model="email">
  
        <label> Password: </label>
        <input type="password" required v-model="password">
        <div v-if="passwordError" class="error">{{ passwordError }}</div>
        
        <label>Phone Number </label>
        <input type="phone" v-model="tempSkill" @keyup="addSkill">

        <label>Address </label>
        <input type="text" v-model="tempSkill" @keyup="addSkill">
    
        <label>License Plate </label>
        <input type="text" v-model="tempSkill" @keyup="addSkill">
    
  
        <div class="terms">
            <input type="checkbox" required v-model="terms">
            <label> Accept terms and conditions </label>
        </div>
  
        <div class="submit">
            <button>Save</button>
        </div>
      </form>
    </div>
</template>
  
    
<script>
    export default {
        data() {
            return {
                email: '',
                password: '',
                terms: false,
                tempSkill: '',
                skills: [], 
                passwordError: ''
            }
        },
        methods: {
            addSkill(e) {
                // console.log(e)
                if (e.key === 'Enter' && this.tempSkill){
                    if(!this.skills.includes(this.tempSkill)){
                        this.skills.push(this.tempSkill)
                    }
                    this.tempSkill = ''
                }
            },
            deleteSkill(skill) {
                this.skills = this.skills.filter((item) => {
                    return skill !== item
                })
            },
            handleSubmit() {
                console.log('Form submitted')
                // alert('Information has changed')
                this.passwordError = this.password.length < 4 ? 'Password must be at least 4 chars long' : ''
    
                if(!this.passwordError) {
                    console.log('Email: ', this.email)
                    console.log('Password: ', this.password)
                    alert('Information changed')
                }
            }
        }
    }
</script>
    
<style scoped>
     form {
        max-width: 420px;
        margin: 30px auto;
        background: white;
        text-align: left;
        padding: 40px;
        border-radius: 10px;
     }
     label {
        color: #aaa;
        display: inline-block;
        margin: 25px 0 15px;
        font-size: 0.6em;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: bold;  
     }
     input {
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 1px solid #ddd;
        color: #555;
     }
     input, select {
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 1px solid #ddd;
        color: #555;
     }
     input[type="checkbox"] {
        display: inline-block;
        width: 16px;
        margin: 0 10px 0 0;
        position: relative;
        top: 2px;
     }
     .pill {
        display: inline-block;
        margin: 20px 10px 0 0;
        padding: 6px 12px;
        background: #eee;
        border-radius: 20px;
        font-size: 12px;
        letter-spacing: 1px;
        font-weight: bold;
        color: #777;
        cursor: pointer;
     }
     button {
      width: 150px;
      padding: auto;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 18px;
    }

    button:hover {
        background-color: #45a049;
    }
     .submit {
        text-align: center;
     }
     .error {
        color: #ff0062;
        margin-top: 10px;
        font-size: 0.8em;
        font-weight: bold;
     }
</style>