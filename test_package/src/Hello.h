/**
 * Autogenerated by Thrift Compiler (0.9.3)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
#ifndef Hello_H
#define Hello_H

#include <thrift/TDispatchProcessor.h>
#include <thrift/async/TConcurrentClientSyncInfo.h>
#include "hello_types.h"



#ifdef _WIN32
  #pragma warning( push )
  #pragma warning (disable : 4250 ) //inheriting methods via dominance 
#endif

class HelloIf {
 public:
  virtual ~HelloIf() {}
  virtual void SayMyName(const std::string& name) = 0;
};

class HelloIfFactory {
 public:
  typedef HelloIf Handler;

  virtual ~HelloIfFactory() {}

  virtual HelloIf* getHandler(const ::apache::thrift::TConnectionInfo& connInfo) = 0;
  virtual void releaseHandler(HelloIf* /* handler */) = 0;
};

class HelloIfSingletonFactory : virtual public HelloIfFactory {
 public:
  HelloIfSingletonFactory(const boost::shared_ptr<HelloIf>& iface) : iface_(iface) {}
  virtual ~HelloIfSingletonFactory() {}

  virtual HelloIf* getHandler(const ::apache::thrift::TConnectionInfo&) {
    return iface_.get();
  }
  virtual void releaseHandler(HelloIf* /* handler */) {}

 protected:
  boost::shared_ptr<HelloIf> iface_;
};

class HelloNull : virtual public HelloIf {
 public:
  virtual ~HelloNull() {}
  void SayMyName(const std::string& /* name */) {
    return;
  }
};

typedef struct _Hello_SayMyName_args__isset {
  _Hello_SayMyName_args__isset() : name(false) {}
  bool name :1;
} _Hello_SayMyName_args__isset;

class Hello_SayMyName_args {
 public:

  Hello_SayMyName_args(const Hello_SayMyName_args&);
  Hello_SayMyName_args& operator=(const Hello_SayMyName_args&);
  Hello_SayMyName_args() : name() {
  }

  virtual ~Hello_SayMyName_args() throw();
  std::string name;

  _Hello_SayMyName_args__isset __isset;

  void __set_name(const std::string& val);

  bool operator == (const Hello_SayMyName_args & rhs) const
  {
    if (!(name == rhs.name))
      return false;
    return true;
  }
  bool operator != (const Hello_SayMyName_args &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const Hello_SayMyName_args & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};


class Hello_SayMyName_pargs {
 public:


  virtual ~Hello_SayMyName_pargs() throw();
  const std::string* name;

  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};


class Hello_SayMyName_result {
 public:

  Hello_SayMyName_result(const Hello_SayMyName_result&);
  Hello_SayMyName_result& operator=(const Hello_SayMyName_result&);
  Hello_SayMyName_result() {
  }

  virtual ~Hello_SayMyName_result() throw();

  bool operator == (const Hello_SayMyName_result & /* rhs */) const
  {
    return true;
  }
  bool operator != (const Hello_SayMyName_result &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const Hello_SayMyName_result & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};


class Hello_SayMyName_presult {
 public:


  virtual ~Hello_SayMyName_presult() throw();

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);

};

class HelloClient : virtual public HelloIf {
 public:
  HelloClient(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> prot) {
    setProtocol(prot);
  }
  HelloClient(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> iprot, boost::shared_ptr< ::apache::thrift::protocol::TProtocol> oprot) {
    setProtocol(iprot,oprot);
  }
 private:
  void setProtocol(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> prot) {
  setProtocol(prot,prot);
  }
  void setProtocol(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> iprot, boost::shared_ptr< ::apache::thrift::protocol::TProtocol> oprot) {
    piprot_=iprot;
    poprot_=oprot;
    iprot_ = iprot.get();
    oprot_ = oprot.get();
  }
 public:
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> getInputProtocol() {
    return piprot_;
  }
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> getOutputProtocol() {
    return poprot_;
  }
  void SayMyName(const std::string& name);
  void send_SayMyName(const std::string& name);
  void recv_SayMyName();
 protected:
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> piprot_;
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> poprot_;
  ::apache::thrift::protocol::TProtocol* iprot_;
  ::apache::thrift::protocol::TProtocol* oprot_;
};

class HelloProcessor : public ::apache::thrift::TDispatchProcessor {
 protected:
  boost::shared_ptr<HelloIf> iface_;
  virtual bool dispatchCall(::apache::thrift::protocol::TProtocol* iprot, ::apache::thrift::protocol::TProtocol* oprot, const std::string& fname, int32_t seqid, void* callContext);
 private:
  typedef  void (HelloProcessor::*ProcessFunction)(int32_t, ::apache::thrift::protocol::TProtocol*, ::apache::thrift::protocol::TProtocol*, void*);
  typedef std::map<std::string, ProcessFunction> ProcessMap;
  ProcessMap processMap_;
  void process_SayMyName(int32_t seqid, ::apache::thrift::protocol::TProtocol* iprot, ::apache::thrift::protocol::TProtocol* oprot, void* callContext);
 public:
  HelloProcessor(boost::shared_ptr<HelloIf> iface) :
    iface_(iface) {
    processMap_["SayMyName"] = &HelloProcessor::process_SayMyName;
  }

  virtual ~HelloProcessor() {}
};

class HelloProcessorFactory : public ::apache::thrift::TProcessorFactory {
 public:
  HelloProcessorFactory(const ::boost::shared_ptr< HelloIfFactory >& handlerFactory) :
      handlerFactory_(handlerFactory) {}

  ::boost::shared_ptr< ::apache::thrift::TProcessor > getProcessor(const ::apache::thrift::TConnectionInfo& connInfo);

 protected:
  ::boost::shared_ptr< HelloIfFactory > handlerFactory_;
};

class HelloMultiface : virtual public HelloIf {
 public:
  HelloMultiface(std::vector<boost::shared_ptr<HelloIf> >& ifaces) : ifaces_(ifaces) {
  }
  virtual ~HelloMultiface() {}
 protected:
  std::vector<boost::shared_ptr<HelloIf> > ifaces_;
  HelloMultiface() {}
  void add(boost::shared_ptr<HelloIf> iface) {
    ifaces_.push_back(iface);
  }
 public:
  void SayMyName(const std::string& name) {
    size_t sz = ifaces_.size();
    size_t i = 0;
    for (; i < (sz - 1); ++i) {
      ifaces_[i]->SayMyName(name);
    }
    ifaces_[i]->SayMyName(name);
  }

};

// The 'concurrent' client is a thread safe client that correctly handles
// out of order responses.  It is slower than the regular client, so should
// only be used when you need to share a connection among multiple threads
class HelloConcurrentClient : virtual public HelloIf {
 public:
  HelloConcurrentClient(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> prot) {
    setProtocol(prot);
  }
  HelloConcurrentClient(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> iprot, boost::shared_ptr< ::apache::thrift::protocol::TProtocol> oprot) {
    setProtocol(iprot,oprot);
  }
 private:
  void setProtocol(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> prot) {
  setProtocol(prot,prot);
  }
  void setProtocol(boost::shared_ptr< ::apache::thrift::protocol::TProtocol> iprot, boost::shared_ptr< ::apache::thrift::protocol::TProtocol> oprot) {
    piprot_=iprot;
    poprot_=oprot;
    iprot_ = iprot.get();
    oprot_ = oprot.get();
  }
 public:
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> getInputProtocol() {
    return piprot_;
  }
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> getOutputProtocol() {
    return poprot_;
  }
  void SayMyName(const std::string& name);
  int32_t send_SayMyName(const std::string& name);
  void recv_SayMyName(const int32_t seqid);
 protected:
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> piprot_;
  boost::shared_ptr< ::apache::thrift::protocol::TProtocol> poprot_;
  ::apache::thrift::protocol::TProtocol* iprot_;
  ::apache::thrift::protocol::TProtocol* oprot_;
  ::apache::thrift::async::TConcurrentClientSyncInfo sync_;
};

#ifdef _WIN32
  #pragma warning( pop )
#endif



#endif
