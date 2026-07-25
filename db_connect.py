import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


@st.cache_resource
def get_connection():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://"
            f"{st.secrets['DB_USER']}:"
            f"{st.secrets['DB_PASSWORD']}@"
            f"{st.secrets['DB_HOST']}:"
            f"{st.secrets['DB_PORT']}/"
            f"{st.secrets['DB_NAME']}"
            f"?sslmode=require",
            pool_pre_ping=True
        )

        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return engine

    except SQLAlchemyError as e:
        st.error(f"Database connection error: {e}")
        return None

    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None