# Recipito - Recipes Marmiton

Recipito is a robust recipe website designed to cater to food enthusiasts just like marmiton.org. Developed using `Python`, `Django`, `HTML`, `CSS` and `JavaScript`, this platform empowers users to create and share their culinary masterpieces, complete with detailed ingredients and utensil models.

## Key Features

- **Recipe Creation**: Users can effortlessly create and share their recipes, providing comprehensive details about the ingredients and utensils required.

- **Admin Approval**: Admin users have the authority to review and approve recipes. Approved recipes are prominently displayed on the home page, complete with user ratings and seamless pagination.

- **Recipe Categories**: Recipes can be optionally categorized, allowing users to explore diverse culinary genres, from drinks and starters to main courses and desserts.

- **User Feedback**: Users can leave valuable feedback on recipes, including comments and ratings, enhancing the overall user experience.

- **French Language Support**: Just like marmiton.org, Recipito primarily operates in French, catering to a Francophone audience.

- **Data Scraping**: The platform scrapes data from marmiton.org using custom commands like 'scrape-recipes' and 'populate-db.' This data includes recipes, ingredients, utensils, and associated images, which are saved in pickle files.

- **User Profiles**: Each user has a profile complete with a profile picture. Email confirmation is also implemented during signup to verify user identity.

- **Admin Control**: An admin panel offers comprehensive control over website content, encompassing recipes, users, and more.

## Getting Started

### For Developers

1. **Clone the Repository**: Download the code by cloning the repository.

2. **Install Dependencies**: Use pipenv to install project dependencies:

   ```bash
   pipenv install
   ```

3. **Create .env File**: Add the following environment variables to your .env file:

   - `SECRET_KEY`: Django secret key for security.
   - `EMAIL_HOST_USER`: Email host user for sending confirmation emails.
   - `EMAIL_HOST_PASSWORD`: Email host password for authentication.

4. **Update `settings.py`**: Modify the `settings.py` file to configure your database settings to point to the provided `test.sqlite3` file, which includes some test data.

5. **Run Migrations**: Execute the following command to apply migrations:

   ```bash
   python manage.py migrate
   ```

### Using Sample Pickle Files

Sample pickle files are provided for convenience. Developers can use these files or run custom commands to create new pickle files from marmiton.org data.

Recipito is a comprehensive platform designed for food enthusiasts and home chefs, combining ease of use with a rich feature set. It empowers users to explore, create, and share their culinary passions seamlessly.

Feel free to reach out for further assistance or to discuss potential collaborations.


This `README.md` provides an overview of the project, its features, and instructions for developers to get started.

### [Screenshots](./screenshots/)
