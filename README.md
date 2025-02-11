# 🛍️ Django & HTMX Social Media Web app
## **Deployed at**
[Text to Display](https://example.com)


A **full-featured social network web application** built with Django, PostgreSQL, and HTMX.  
This project includes **post publishing, editing, and liking, as well as user following and unfollowing.**

---

## **🚀 Features &  Technologies Used**
✅ **User Authentication** (Register, Login, Logout)  
✅ **User profile page** (Follow, Unfollow users, see their posts and how many followers they have)  
✅ **Post publishing and same-page editing**  
✅ **Liking and unliking posts**  
✅ **"Infinite scroll" using Django pagination**  
✅ **Light-weight interactivity using HTMX**  


---

## **📦 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/ThisisAngelina/social_network.git
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
cd .. # Go back to the root directory
pip install -r requirements.txt
```
### **4️⃣ Configure Environment Variables**

For this project, you only need to set the Django SECRET_KEY to a random string.

### **5️⃣ Populate the database**

In settings.py, specify sqlite3 as your database

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",  # Stores the database file in the project root
    }
}
```

You can then upload sample posts manually or user the **faker** library.


### **6️⃣ Apply Migrations & Create Superuser**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### **7️⃣ Set your DEBUG=TRUE in settings.py and run your local server:**

```bash
python manage.py runserver
```

## **📜 License**

This project is licensed under the MIT License.