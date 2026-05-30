# St. Antony's Girls Higher Secondary School Website

A complete, clean, modern, and professional web portal for **St. Antony's Girls Higher Secondary School**, Chennai.

Built using a premium, soft, feminine, and scholarly aesthetic featuring Deep Maroon, Cream, Gold, and Soft Sage Green accents. The site is fully responsive, mobile-friendly, and offers multiple interactive client-side features powered by Vanilla Javascript and Python Flask.

## Tech Stack & Features

- **Backend:** Python Flask
- **Frontend:** HTML5, Vanilla CSS3 (custom responsive design system), Vanilla JavaScript
- **Assets:** Custom generated school crest/logo, curated educational photography Unsplash mappings
- **Responsive Layout:** Dynamic sticky navigation, glassmorphism mobile menu drawer
- **Animations:** Custom CSS scroll-triggered fade-in and slide-up elements using `IntersectionObserver`
- **Interactions:**
  - Dynamic Hero Banner with automatic and interactive image slideshow carousel
  - Filterable Media Gallery with customized image lightbox viewer
  - Interactive Admissions guide accordion
  - Form validation and AJAX submission handlers (Admissions Inquiry and Contact Us) with loading and success/error status UI overlays

---

## Directory Structure

```
d:/Aventro Clients/ST/
├── app.py                  # Main Flask application with routing & mock APIs
├── requirements.txt        # Backend dependencies
├── README.md               # Project documentation
├── static/
│   ├── css/
│   │   └── style.css       # Global layout, color variables & page-specific styles
│   ├── js/
│   │   └── main.js         # Navigation, animations, slideshow, filtering & form processing
│   └── images/
│       └── logo.png        # Generated school crest/logo
└── templates/
    ├── base.html           # Unified wrapper structure (header, footer, meta-properties)
    ├── index.html          # Homepage (principal note, highlights, events)
    ├── about.html          # History, values, and school leadership faculty
    ├── academics.html      # Curriculum, streams offered, and achievements board
    ├── admissions.html     # Timelines, guidelines, and interactive inquiry form
    ├── gallery.html        # Multi-category media grid & lightbox modals
    └── contact.html        # Map coordinates, contact cards, and feedback messaging
```

---

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Installation

1. Open a terminal (PowerShell / Command Prompt) in the project directory:
   ```bash
   cd "d:/Aventro Clients/ST"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

To launch the local development server:

```bash
python app.py
```

The application will start running on [http://localhost:5000](http://localhost:5000). You can navigate through the pages and test the interactive form submissions.

---

## Design Customizations

The look and feel is managed completely via CSS custom variables in `static/css/style.css`. Feel free to adjust these values to update colors or fonts:

```css
:root {
    --color-maroon: #800000;         /* Primary Brand Color */
    --color-cream-bg: #F5F0E6;       /* Editorial light background */
    --color-gold: #D4AF37;           /* Accent and Borders */
    --color-sage: #688A7E;           /* Success Indicators and Badges */
    ...
}
```
