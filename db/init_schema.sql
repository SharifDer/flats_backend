-- Create the 'users' table if it does not exist
CREATE TABLE IF NOT EXISTS users (
    firebase_id VARCHAR(255) PRIMARY KEY,    -- Firebase ID is the primary key
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    user_type VARCHAR(130) NOT NULL,         -- Type of user (could be "admin", "tenant", etc.)
    phone_number VARCHAR(15) NOT NULL

);

-- Create the 'apartments' table if it does not exist
CREATE TABLE IF NOT EXISTS apartments (
    id SERIAL PRIMARY KEY,                  -- Auto-incremented ID for each apartment
    firebase_id_user VARCHAR(255),           -- Firebase ID of the user who posted the apartment
    title VARCHAR(255) NOT NULL,             -- Title of the apartment
    type VARCHAR(100) NOT NULL,              -- Type of the apartment (e.g., "2BHK", "Studio")
    address TEXT NOT NULL,                   -- Address of the apartment
    price DECIMAL(10, 2) NOT NULL,           -- Price of the apartment
    number_of_rooms INT,                    -- Number of rooms
    number_of_bathrooms INT,                -- Number of bathrooms
    description TEXT,                       -- Description of the apartment
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of when the apartment is posted
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the apartment details are updated
    status BOOLEAN NOT NULL,
    FOREIGN KEY (firebase_id_user) REFERENCES users(firebase_id) ON DELETE CASCADE  -- Foreign key linking to 'users'
);

-- Create the 'apartment_images' table if it does not exist
CREATE TABLE IF NOT EXISTS apartment_images (
    image_id SERIAL PRIMARY KEY,            -- Auto-incremented ID for each image
    apartment_id INT NOT NULL,              -- Apartment ID to associate the image with a specific apartment
    image_url TEXT NOT NULL,                -- URL or path to the image
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the image was added
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the image was last updated
    FOREIGN KEY (apartment_id) REFERENCES apartments(id) ON DELETE CASCADE  -- Foreign key linking to 'apartments'
);
