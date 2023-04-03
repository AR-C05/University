// 16-01-2023
// AR
// 3388 A1

#include <GLFW/glfw3.h>

int main(void) {
    GLFWwindow *window;

    // initializes the glfw library
    if (!glfwInit()) {
        return -1;
    }

    // Create a windowed mode window and its OpenGL context
    // dimensions 1280px by 1000px and title "Hello World"
    window = glfwCreateWindow(1280, 1000, "Hello World", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }

    // Make the window's context current
    glfwMakeContextCurrent(window);
    
    // Loop until the user closes the window
    while (!glfwWindowShouldClose(window))
    {
        // Poll for and process events 
        glfwPollEvents();
        
        // Render here
        glClear(GL_COLOR_BUFFER_BIT);

        // displaying the triangle
        // colour the triangle
        glColor3b(58, 7, 97);

        // begin drawing the triangle
        glBegin(GL_TRIANGLES);
        glVertex2f(0, 0.5);
        glVertex2f(0.5, -0.25);
        glVertex2f(-0.5, -0.25);
        // end drawing triangle
        glEnd();
        
        // Swap front and back buffers 
        glfwSwapBuffers(window);

    }

    glfwTerminate();
    return 0;
}
