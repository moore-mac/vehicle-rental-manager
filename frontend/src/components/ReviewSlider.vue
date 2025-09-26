<script setup>
import { ref, onMounted } from "vue";

const reviews = ref([
  {
    name: "Alice M.",
    location: "London",
    rating: 5,
    text: "Great service and very clean cars!",
  },
  {
    name: "John D.",
    location: "Manchester",
    rating: 4,
    text: "Smooth booking process, friendly staff.",
  },
  {
    name: "Emma W.",
    location: "Bristol",
    rating: 5,
    text: "Loved the variety of vehicles, highly recommend!",
  },
  {
    name: "Carlos P.",
    location: "Liverpool",
    rating: 4,
    text: "Affordable prices and excellent support.",
  },
  {
    name: "Sophia R.",
    location: "Leeds",
    rating: 5,
    text: "The car was in perfect condition, amazing experience.",
  },
  {
    name: "Liam T.",
    location: "Birmingham",
    rating: 5,
    text: "Booking was effortless and the staff were very helpful.",
  },
  {
    name: "Mia S.",
    location: "Glasgow",
    rating: 4,
    text: "Car quality was excellent, minor delay on pickup but overall good.",
  },
  {
    name: "Ethan R.",
    location: "Nottingham",
    rating: 5,
    text: "Fantastic service! The vehicle was spotless and comfortable.",
  },
  {
    name: "Olivia K.",
    location: "Sheffield",
    rating: 4,
    text: "Good value for money, smooth experience renting the car.",
  },
  {
    name: "Noah B.",
    location: "Cardiff",
    rating: 5,
    text: "Highly recommend this rental service, very professional and friendly staff.",
  },
]);

const currentIndex = ref(0);
const total = reviews.value.length;

function next() {
  currentIndex.value = (currentIndex.value + 1) % total;
}

onMounted(() => {
  setInterval(next, 3000);
});
</script>

<template>
  <div class="reviews-carousel">
    <h1>Customer Reviews</h1>

    <div class="carousel-container">
      <div
        class="carousel-track"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div
          class="review-card"
          v-for="(review, index) in reviews"
          :key="index"
        >
          <p class="quote">“{{ review.text }}”</p>
          <div class="reviewer">
            <strong>{{ review.name }}</strong> -
            <span>{{ review.location }}</span>
          </div>
          <div class="rating">
            <span
              v-for="rating in 5"
              :key="rating"
              class="star"
              :class="{ filled: rating <= review.rating }"
              >★</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reviews-carousel {
  max-width: 800px;
  margin: 3rem auto;
  padding: 1rem;
  text-align: center;
  position: relative;
}

.carousel-container {
  overflow: hidden;
  position: relative;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.review-card {
  min-width: 100%;
  padding: 2rem;
}

.quote {
  font-style: italic;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.reviewer {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.rating .star {
  color: #ddd;
  font-size: 1rem;
}

.rating .star.filled {
  color: #fbbf24;
}

button.prev,
button.next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  font-size: 2rem;
  padding: 0.2rem 0.6rem;
  border-radius: 50%;
  cursor: pointer;
}

button.prev {
  left: 0.5rem;
}
button.next {
  right: 0.5rem;
}

button.prev:hover,
button.next:hover {
  background: rgba(0, 0, 0, 0.8);
}
</style>
