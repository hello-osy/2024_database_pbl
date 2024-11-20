<template>
    <!-- My Profile Section -->
      <div class="my-profile">
        <h3>My Profile</h3>
        <div class="profile-details">
          <img :src="profile.photo" alt="Driver's Photo" class="profile-photo">
          <div class="profile-info">
            <p><strong>Name:</strong> {{ profile.name }}</p>
            <p><strong>Phone Number:</strong> {{ profile.phoneNumber }}</p>
            <p><strong>Address:</strong> {{ profile.address }}</p>
            <p><strong>Current Location:</strong> {{ currentLocation }}</p>
            <div class="about-me">
              <h4>About Me</h4>
              <p>{{ profile.about }}</p>
            </div>
          </div>
        </div>
      </div>
    
</template>
    
<script>
    export default {
        name: 'DriverProfile',
        props: {},
        data(){
          return {
          // Existing data properties
            status: 'Available',
            nextTrip: {
            time: '10:30 AM',
            destination: 'City Center'
            },
            currentLocation: '123 Main St, City Center',
            revenue: 1345.00,
            showDropDown: false,
          // Profile data
            profile: {
              photo: 'path/to/photo.jpg', // Path to the driver's photo
              name: 'John Doe',
              phoneNumber: '123-456-7890',
              address: '456 Elm St, City Center',
              about: 'Experienced driver with over 10 years in the industry. Passionate about safety and excellent customer service.'
            }
        }
      }
    }
    
</script>
    
<style>
    /* My Profile Section */
    .my-profile {
      margin-top: 20px;
      padding: 20px;
      border-top: 2px solid #ddd;
      background-color: #f0f2f5; /* Light background for contrast */
      border-radius: 8px;
    }
    
    .my-profile h3 {
      font-size: 1.6rem;
      color: #444;
      margin-bottom: 20px;
      font-weight: bold;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Profile Details Layout */
    .profile-details {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    
    /* Profile Photo Styling */
    .profile-photo {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      object-fit: cover;
      border: 3px solid #ccc;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease;
    }
    
    .profile-photo:hover {
      transform: scale(1.05);
    }
    
    /* Profile Info Styling */
    .profile-info {
      font-size: 1rem;
      color: #333;
    }
    
    .profile-info p {
      margin: 8px 0;
      line-height: 1.4;
    }
    
    .profile-info p strong {
      color: #555;
    }
    
    /* About Me Section */
    .about-me {
      margin-top: 15px;
      background-color: #fff;
      padding: 10px;
      border-radius: 6px;
      border: 1px solid #ddd;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .about-me h4 {
      font-size: 1.2rem;
      color: #666;
      margin-bottom: 10px;
      font-weight: bold;
    }
    
    .about-me p {
      font-size: 0.95rem;
      color: #555;
      line-height: 1.5;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
      .profile-details {
        flex-direction: column;
        align-items: flex-start;
      }
    
      .profile-photo {
        width: 100px;
        height: 100px;
      }
    }
    
    @media (max-width: 480px) {
      .profile-photo {
        width: 80px;
        height: 80px;
      }
    
      .my-profile h3 {
        font-size: 1.4rem;
      }
    
      .about-me h4 {
        font-size: 1.1rem;
      }
    
      .about-me p {
        font-size: 0.9rem;
      }
    }
    
    
</style>
    