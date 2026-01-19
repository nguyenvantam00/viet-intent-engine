#include "viet_intent.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(viet_intent, m) {
  m.doc() = "Vietnamese Intent Detection Engine";

  py::class_<VietIntent::IntentResult>(m, "IntentResult")
      .def(py::init<>())
      .def_readwrite("intent", &VietIntent::IntentResult::intent)
      .def_readwrite("confidence", &VietIntent::IntentResult::confidence)
      .def_readwrite("entities", &VietIntent::IntentResult::entities)
      .def_readwrite("response_pattern",
                     &VietIntent::IntentResult::response_pattern)
      .def("__repr__", [](const VietIntent::IntentResult &r) {
        return "<IntentResult intent='" + r.intent +
               "' confidence=" + std::to_string(r.confidence) + ">";
      });

  py::class_<VietIntent::IntentEngine>(m, "IntentEngine")
      .def(py::init<>())
      .def("initialize", &VietIntent::IntentEngine::initialize,
           py::arg("model_path") = "models/")
      .def("detect", &VietIntent::IntentEngine::detect)
      .def("add_intent", &VietIntent::IntentEngine::add_intent)
      .def("load_patterns_from_file",
           &VietIntent::IntentEngine::load_patterns_from_file)
      .def("save_patterns", &VietIntent::IntentEngine::save_patterns);

  m.def("create_engine",
        []() { return std::make_unique<VietIntent::IntentEngine>(); });
}
