// 17-02-2023
// AR
// 3388 A3 pen tool

#include <GLFW/glfw3.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <cmath>

struct Point {
    float x, y;
};

struct Node : Point {
    bool hasHandle1, hasHandle2;
    Point handle1, handle2;
};

// returns value for the cubic bezier curve for the spline
float cubicBez(float a, float c1, float c2, float b, float t) {
    // (1-t)^3 * A
    float A = (1-t) * (1-t) * (1-t) * a;
    // 3(1-t)^2 t * C1
    float C1 = 3 * (1-t) * (1-t) * t * c1;
    // 3(1-t) t^2 * C2
    float C2 = 3 * (1-t) * t * t * c2;
    // t^3 * B
    float B = t * t * t * b;

    return A + C1 + C2 + B;
}

// creates a node based at given coordinates
Node* createNode(float x_val, float y_val, bool h1, bool h2) {
    Node *n = new Node();
    n->hasHandle1 = h1;
    n->hasHandle2 = h2;
    if (h1) {
        n->handle1 = *(new Point());
        n->handle1.x = x_val;
        n->handle1.y = y_val + 50;
    }
    if (h2) {
        n->handle2 = *(new Point());
        n->handle2.x = x_val;
        n->handle2.y = y_val + 50;
    }
    n->x = x_val;
    n->y = y_val;

    return n;
}

int main(int argc, char **argv) {

    if (argc != 3) {
        std::cerr << "Usage: ./executable WIDTH_int HEIGHT_int" << std::endl;
        exit(-1);
    }

    int width, height;

    width = atoi(argv[1]);
    height = atoi(argv[2]);

    GLFWwindow *window;

    // initializes the glfw library
    if (!glfwInit()) {
        return -1;
    }

    // enable 4x multisampling
    glfwWindowHint(GLFW_SAMPLES, 4);
    glEnable(GL_MULTISAMPLE);

    // Create a windowed mode window and its OpenGL context
    window = glfwCreateWindow(width, height, "A3 Pen Tool", NULL, NULL);
    if (!window) {
        glfwTerminate();
        return -1;
    }

    // Make the window's context current
    glfwMakeContextCurrent(window);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    // viewing volume
    glOrtho (0, width, 0, height, -1, 1);
    glViewport(0, 0, width, height);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // all the nodes
    std::vector<Node> nodes;
    int numNodes;

    double mouseX, mouseY;
    bool mousePressed = false;
    int mouseTime = 0, mouseAction;
    bool nodeSelected = false, controlPointSelected = false;
    int selNodeIndex, selControlPoint;

    // Loop until the user closes the window
    while (!glfwWindowShouldClose(window)) {
        // Poll for and process events (mouse/keyboard)
        glfwPollEvents();

        // reset on user pressing E
        if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS) {
            nodes.clear();
        }

        glfwGetCursorPos(window, &mouseX, &mouseY);
        mouseY = height - mouseY;
        
        mouseAction = glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT);
        numNodes = nodes.size();
        // mouse press left button
        if ( mouseAction == GLFW_PRESS) {
            mouseTime++;
            if (mouseTime >= 3) {
                mousePressed = true;
            }
            // is mouse press on a node or control point:
            for (int i = 0; i < numNodes; i++) {
                // clicked on node
                if (nodes[i].x - 5 <= mouseX && nodes[i].x + 5 >= mouseX &&
                    nodes[i].y - 5 <= mouseY && nodes[i].y + 5 >= mouseY) {
                        nodeSelected = true;
                        selNodeIndex = i;
                }
                // clicked on handle 1 of the node
                else if (nodes[i].hasHandle1 && 
                    nodes[i].handle1.x - 5 <= mouseX && nodes[i].handle1.x + 5 >= mouseX &&
                    nodes[i].handle1.y - 5 <= mouseY && nodes[i].handle1.y + 5 >= mouseY) {
                    controlPointSelected = true;
                    selControlPoint = 1;
                    selNodeIndex = i;
                }
                // clicked on handle 2 of the node
                else if (nodes[i].hasHandle2 && 
                    nodes[i].handle2.x - 5 <= mouseX && nodes[i].handle2.x + 5 >= mouseX &&
                    nodes[i].handle2.y - 5 <= mouseY && nodes[i].handle2.y + 5 >= mouseY) {
                    controlPointSelected = true;
                    selControlPoint = 2;
                    selNodeIndex = i;
                }
            }
            if (mousePressed) {
                // pressed on node
                if (nodeSelected) {
                    // move selected node and its handles
                    double dX = mouseX - nodes[selNodeIndex].x;
                    double dY = mouseY - nodes[selNodeIndex].y;
                    nodes[selNodeIndex].x = mouseX;
                    nodes[selNodeIndex].y = mouseY;
                    if (nodes[selNodeIndex].hasHandle1) {
                        nodes[selNodeIndex].handle1.x += dX;
                        nodes[selNodeIndex].handle1.y += dY;
                    }
                    if (nodes[selNodeIndex].hasHandle2) {
                        nodes[selNodeIndex].handle2.x += dX;
                        nodes[selNodeIndex].handle2.y += dY;
                    }
                }
                // pressed on a control point
                else if (controlPointSelected) {
                    // moving handle 1
                    if (selControlPoint == 1) {
                        nodes[selNodeIndex].handle1.x = mouseX;
                        nodes[selNodeIndex].handle1.y = mouseY;
                        // sync handle 2 (if it exists)
                        if (nodes[selNodeIndex].hasHandle2) {
                            // deltaX between handle1 and node
                            double dHx = nodes[selNodeIndex].handle1.x - nodes[selNodeIndex].x;
                            // deltaY between handle1 and node
                            double dHy = nodes[selNodeIndex].handle1.y - nodes[selNodeIndex].y;
                            nodes[selNodeIndex].handle2.x = nodes[selNodeIndex].x - dHx;
                            nodes[selNodeIndex].handle2.y = nodes[selNodeIndex].y - dHy;
                        }
                    }
                    // moving handle 2
                    else if (selControlPoint == 2) {
                        nodes[selNodeIndex].handle2.x = mouseX;
                        nodes[selNodeIndex].handle2.y = mouseY;
                        // sync handle 1 (if it exists)
                        if (nodes[selNodeIndex].hasHandle1) {
                            // deltaX between handle1 and node
                            double dHx = nodes[selNodeIndex].handle2.x - nodes[selNodeIndex].x;
                            // deltaY between handle1 and node
                            double dHy = nodes[selNodeIndex].handle2.y - nodes[selNodeIndex].y;
                            nodes[selNodeIndex].handle1.x = nodes[selNodeIndex].x - dHx;
                            nodes[selNodeIndex].handle1.y = nodes[selNodeIndex].y - dHy;
                        }
                    }
                }
            }
        }
        else if (mouseAction == GLFW_RELEASE && mousePressed) {
            // adding new node
            if (nodeSelected == false && controlPointSelected == false) {
                // first node
                if (nodes.size() == 0) {
                    nodes.push_back(*createNode(mouseX, mouseY, false, false));
                }
                // second node
                else if (nodes.size() == 1) {
                    if (mouseX < nodes[0].x) {
                        nodes[0].hasHandle1 = true;
                        nodes[0].handle1.x = nodes[0].x;
                        nodes[0].handle1.y = nodes[0].y + 50;
                        nodes.insert(nodes.begin() + 0, *createNode(mouseX, mouseY, false, true));
                    } else {
                        nodes[0].hasHandle2 = true;
                        nodes[0].handle2.x = nodes[0].x;
                        nodes[0].handle2.y = nodes[0].y + 50;
                        nodes.push_back(*createNode(mouseX, mouseY, true, false));
                    }
                }
                // other nodes
                else {
                    double dxStart = nodes[0].x - mouseX, dxEnd = nodes[numNodes - 1].x - mouseX;
                    double dyStart = nodes[0].y - mouseY, dyEnd = nodes[numNodes - 1].y - mouseY;
                    double dStart = std::sqrt((dxStart * dxStart) + (dyStart * dyStart));
                    double dEnd = std::sqrt((dxEnd * dxEnd) + (dyEnd * dyEnd));
                    // add to start of spline
                    if (dStart < dEnd) {
                        // deltaX between handle2 and node
                        double dHx = nodes[0].handle2.x - nodes[0].x;
                        // deltaY between handle2 and node
                        double dHy = nodes[0].handle2.y - nodes[0].y;
                        nodes[0].hasHandle1 = true;
                        nodes[0].handle1.x = nodes[0].x - dHx;
                        nodes[0].handle1.y = nodes[0].y - dHy;
                        nodes.insert(nodes.begin() + 0, *createNode(mouseX, mouseY, false, true));
                    }
                    // add to end of spline
                    else {
                        // deltaX between handle1 and node
                        double dHx = nodes[numNodes - 1].handle1.x - nodes[numNodes - 1].x;
                        // deltaY between handle1 and node
                        double dHy = nodes[numNodes - 1].handle1.y - nodes[numNodes - 1].y;

                        nodes[numNodes - 1].hasHandle2 = true;
                        nodes[numNodes - 1].handle2.x = nodes[numNodes - 1].x - dHx;
                        nodes[numNodes - 1].handle2.y = nodes[numNodes - 1].y - dHy;
                        nodes.push_back(*createNode(mouseX, mouseY, true, false));
                    }
                }
            }
            mousePressed = false;
            nodeSelected = false;
            controlPointSelected = false;
            mouseTime = 0;
        }
        
        // ================RENDERING STUFF======================
        // =====================================================
        // clear for white background
        glClearColor(1,1,1,1);
        glClear(GL_COLOR_BUFFER_BIT);
        // draw in black
        glColor3b(0, 0, 0);

        // Render the spline (each piece as an independent cubic Bezier curve)
        // each curve a polyline of 200 line segments
        glEnable(GL_LINE_SMOOTH);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glLineWidth(2.0f);
        glBegin(GL_LINE_STRIP);
            numNodes = nodes.size();
            for (int i = 0; i < numNodes - 1; i++) {
                Node a = nodes[i], b = nodes[i+1];
                for (int j = 0; j < 200; j++) {
                    float t = (float) j;
                    t /= 200;
                    // std::cout << a.x << " " << a.handle2.x << " " << b.handle1.x << " " << b.x << " " << t << " " << std::endl;
                    glVertex2f(cubicBez(a.x, a.handle2.x, b.handle1.x, b.x, t), cubicBez(a.y, a.handle2.y, b.handle1.y, b.y, t));
                }
            }
        glEnd();
        glLineWidth(1.0f);
        glDisable(GL_BLEND);
        glDisable(GL_LINE_SMOOTH);

        // render each node of spline
        glPointSize(10.0f);
        glBegin(GL_POINTS);
            numNodes = nodes.size();
            for (int i = 0; i < numNodes; i++) {
                glVertex2f(nodes[i].x, nodes[i].y);
            }
        glEnd();
        glPointSize(1.0f);

        // render each control point
        glEnable(GL_POINT_SMOOTH);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glPointSize(5.0f);
        glBegin(GL_POINTS);
            numNodes = nodes.size();
            for (int i = 0; i < numNodes; i++) {
                Node a = nodes[i];
                if (a.hasHandle1) {
                    glVertex2f(a.handle1.x, a.handle1.y);
                }
                if (a.hasHandle2) {
                    glVertex2f(a.handle2.x, a.handle2.y);
                }
            }
        glEnd();
        glPointSize(1.0f);
        glDisable(GL_BLEND);
        glDisable(GL_POINT_SMOOTH);

        // dotted lines connecting control points to nodes
        glEnable(GL_LINE_STIPPLE);
        glLineWidth(2.0f);
        glLineStipple(2, 0xAAAA);
        numNodes = nodes.size();
        for (int i=0; i < numNodes; i++) {
            Node a = nodes[i];
            glBegin(GL_LINE_STRIP);
                if (a.hasHandle1) {
                    glVertex2f(a.handle1.x, a.handle1.y);
                }
                glVertex2f(a.x, a.y);
                if (a.hasHandle2) {
                    glVertex2f(a.handle2.x, a.handle2.y);
                }
            glEnd();
        }
        glLineWidth(1.0f);
        glDisable(GL_LINE_STIPPLE);

		// Swap front and back buffers 
        glfwSwapBuffers(window);
    }
}
