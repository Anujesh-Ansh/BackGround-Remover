import streamlit as st
from rembg import remove
from PIL import Image
import io
from io import BytesIO


def main():
    st.session_state.reset = False
    uploadedFile = st.session_state.get("uploadedFile", None)
    computedPicture = st.session_state.get("computedPicture", None)
    PictureSaved = st.session_state.get("PictureSaved", False)
    ShowDownloadArea = st.session_state.get("ShowDownloadArea", False)
    DisableDownloadButton = st.session_state.get("DisableDownloadButton", True)
    individualNumber = st.session_state.get("individualNumber", 0)

    st.title("Background Remover")
    st.write("This app allows you to remove the background from an image.")

    uploadedFile = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png"],
        on_change=resetStates,
        key=f"{individualNumber}",
    )

    if uploadedFile is not None:
        image1 = Image.open(uploadedFile)
        st.image(image1, caption="Uploaded Image", use_column_width=True)
        st.session_state.uploadedFile = image1
        st.session_state.PictureWasChosen = True

    if computedPicture is not None:
        st.image(computedPicture, caption="Result Image", use_column_width=True)

    if uploadedFile:
        if st.button("Remove Background"):
            with st.spinner("Removing background..."):
                result_image = remove(image1)

            st.session_state.computedPicture = result_image
            st.session_state.ShowDownloadArea = True
            ShowDownloadArea = True

            computedPicture = result_image
            st.success("Background removed successfully!")

            st.image(result_image, caption="Result Image", use_column_width=True)

        if ShowDownloadArea:
            with st.form("my_form"):
                save_as = st.text_input("Enter filename to save:")

                if st.form_submit_button("Submit"):
                    if len(save_as) > 0:
                        st.session_state.DisableDownloadButton = False
                        DisableDownloadButton = False

            buf = BytesIO()
            computedPicture.save(buf, format="PNG")
            byte_im = buf.getvalue()

            if PictureSaved:
                st.success("Saved successfully")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.download_button(
                    "Save Result",
                    byte_im,
                    f"{save_as}",
                    mime="image/png",
                    on_click=SetSavedBanner,
                    disabled=DisableDownloadButton,
                )
            with col2:
                if st.button("Upload new image"):
                    resetStates(
                        changeImageIndex=True, individualNumber=individualNumber
                    )
                    st.rerun()


def SetSavedBanner():
    st.session_state.PictureSaved = True


def resetStates(changeImageIndex=False, individualNumber=0):
    st.session_state.uploadedFile = None
    st.session_state.computedPicture = None
    st.session_state.PictureSaved = False
    st.session_state.ShowDownloadArea = False
    st.session_state.DisableDownloadButton = True
    st.session_state.PictureWasChosen = False
    if changeImageIndex:
        st.session_state.individualNumber = individualNumber + 1


if __name__ == "__main__":
    main()
